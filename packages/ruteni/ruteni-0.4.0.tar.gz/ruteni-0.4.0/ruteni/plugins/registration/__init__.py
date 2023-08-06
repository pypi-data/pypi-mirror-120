"User registration"

import logging
from email import message_from_string
from email.errors import MessageDefect, MessageParseError
from email.headerregistry import Address
from email.utils import formataddr
from functools import reduce
from random import randint
from typing import Any, Optional, Union

import limits.storage
import limits.strategies
from pkg_resources import resource_filename
from ruteni import configuration
from ruteni.plugins.database import database
from ruteni.plugins.locale import locales
from ruteni.plugins.passwords import register_user
from ruteni.plugins.session import get_user_from_environ
from ruteni.plugins.users import get_user_by_email
from ruteni.utils.dns import RecordList, query_mx
from ruteni.utils.jinja2 import render_template
from ruteni.utils.smtp import send_mail
from sqlalchemy.sql import select
from starlette.applications import Starlette
from transitions.core import MachineError
from transitions.extensions.asyncio import AsyncMachine
from zxcvbn import zxcvbn

logger = logging.getLogger(__name__)

Issues = dict[str, Union[bool, int, str]]

SITE_NAME: str = configuration.get("RUTENI_SITE_NAME")
FROM_ADDRESS: str = configuration.get("RUTENI_REGISTRATION_FROM_ADDRESS")
ABUSE_URL: str = configuration.get("RUTENI_REGISTRATION_ABUSE_URL")
VERIFICATION_CODE_DIGITS: int = configuration.get(
    "RUTENI_REGISTRATION_VERIFICATION_CODE_DIGITS", cast=int, default=6
)
MINIMUM_PASSWORD_STRENGTH: int = configuration.get(
    "RUTENI_REGISTRATION_MINIMUM_PASSWORD_STRENGTH", cast=int, default=3
)
MAXIMUM_DISPLAY_NAME_LENGTH: int = configuration.get(
    "RUTENI_REGISTRATION_MAXIMUM_DISPLAY_NAME_LENGTH", cast=int, default=40
)
MAXIMUM_EMAIL_LENGTH: int = configuration.get(
    "RUTENI_REGISTRATION_MAXIMUM_EMAIL_LENGTH", cast=int, default=40
)
MAXIMUM_PASSWORD_LENGTH: int = configuration.get(
    "RUTENI_REGISTRATION_MAXIMUM_PASSWORD_LENGTH", cast=int, default=40
)

KNOWN_LOCALES = ("en-EN", "fr-FR")  # TODO: from available emails

# https://limits.readthedocs.org
# https://haliphax.dev/2021/03/rate-limiting-with-flask-socketio/
# https://pypi.org/project/fastapi-limiter/

# uri = "redis+unix:///var/run/redis/redis-server.sock"
# options: dict = {}
# redis_storage = limits.storage.storage_from_string(uri, **options)
memory_storage = limits.storage.MemoryStorage()
one_per_second = limits.RateLimitItemPerSecond(1, 1)
moving_window = limits.strategies.MovingWindowRateLimiter(memory_storage)


class Registration:
    "User registration"

    def __init__(self) -> None:
        self.display_name: Optional[str] = None
        self.email: Optional[str] = None
        self.password: Optional[str] = None
        self.locale: Optional[str] = None
        self.records: Optional[RecordList] = None
        self.verification_code: Optional[str] = None
        self.issues: dict[str, Issues] = dict(
            display_name={}, email={}, password={}, locale={}
        )

    async def input_ok(
        self, rv: list, *, display_name: str, email: str, password: str, locale: str
    ) -> bool:
        "Set the registration information"
        if self.display_name != display_name:
            issues = self.issues["display_name"]
            issues.clear()
            if display_name == "":
                issues["invalid-display-name"] = "empty"
            elif len(display_name) > MAXIMUM_DISPLAY_NAME_LENGTH:
                issues["invalid-display-name"] = "overflow"
            self.display_name = display_name

        if self.email != email:
            issues = self.issues["email"]
            issues.clear()
            if len(email) == 0:
                issues["invalid-email"] = "empty"
            elif len(email) > MAXIMUM_EMAIL_LENGTH:
                issues["invalid-email"] = "overflow"
            elif "@" not in email or (
                len(email) > 1 and email[-1] == "@" and "@" not in email[:-1]
            ):
                # input is something like `foo` or 'foo@'
                try:
                    email.encode("ascii")
                except UnicodeEncodeError:
                    issues["invalid-email"] = "parse-error"
                else:
                    issues["invalid-email"] = "incomplete"
            else:
                try:
                    address = Address(display_name=display_name, addr_spec=email)
                except (IndexError, MessageDefect, MessageParseError):
                    issues["invalid-email"] = "parse-error"
                else:
                    logger.debug(f"resolving MX for {address.domain}")
                    records = await query_mx(address.domain)
                    if records is None:
                        issues["invalid-email"] = "unknown-domain"
                    else:
                        logger.debug(f"found records: {records}")
                        if len(records):
                            self.records = sorted(records, key=lambda rec: rec.priority)
                        else:
                            issues["invalid-email"] = "misconfigured-domain"
            self.email = email

        if self.password != password:
            issues = self.issues["password"]
            issues.clear()
            if len(password) == 0:
                issues["invalid-password"] = "empty"
            elif len(password) > MAXIMUM_EMAIL_LENGTH:
                issues["invalid-password"] = "overflow"
            else:
                results = zxcvbn(password, user_inputs=[display_name, email])
                if results["score"] < MINIMUM_PASSWORD_STRENGTH:
                    issues["low-password-strength"] = results["score"]
            self.password = password

        if self.locale != locale:
            issues = self.issues["locale"]
            issues.clear()
            if locale == "":
                issues["invalid-locale"] = "empty"
            else:
                locale_id = await database.fetch_val(
                    select([locales.c.id]).where(locales.c.code == locale)
                )
                if locale_id is None:
                    issues["invalid-locale"] = "unknown"
            self.locale = locale

        issues = reduce(lambda a, b: {**a, **b}, self.issues.values())
        rv.append(issues)
        return len(issues) == 0

    async def sent_ok(self, rv: list) -> bool:
        # ignore registration if an active user with the same email exists
        assert self.email
        user_info = await get_user_by_email(self.email)
        if user_info is not None:
            # TODO: do everything but send the email to protect users' privacy? by
            # timing a failed registration, one could deduce that a user has an account
            rv.append(False)
            return False

        random_code = randint(0, 10 ** VERIFICATION_CODE_DIGITS - 1)
        self.verification_code = f"{{:0{VERIFICATION_CODE_DIGITS}}}".format(random_code)

        template_path = resource_filename(
            __name__,
            f"emails/{self.locale}/verification.html",
        )
        logger.debug(f"email template: {template_path}")
        params = {
            "email": self.email,
            "from": FROM_ADDRESS,
            "to": formataddr((self.display_name, self.email)),  # type: ignore
            "display_name": self.display_name,
            "site_name": SITE_NAME,
            "verification_code": self.verification_code,
            "abuse_url": ABUSE_URL,
        }
        content = await render_template(template_path, params)
        message = message_from_string(content)
        logger.debug(message)

        for record in self.records:  # type: ignore
            if await send_mail(message, record.host):
                rv.append(True)
                return True

        logger.debug("could not deliver email")
        rv.append(False)
        return False

    async def code_ok(self, rv: list, code: str) -> bool:
        correct = self.verification_code == code
        logger.debug("code_ok", correct)
        if correct:
            assert self.display_name and self.email and self.locale and self.password
            user_id, password_id = await register_user(
                self.display_name, self.email, self.locale, self.password
            )

            logger.debug(
                "account created:", user_id, self.display_name, self.email, password_id
            )

            # print(await group_manager.add_user_to_group(user_id, "admin"))

        rv.append(correct)
        return correct


TRANSITIONS = (
    {"trigger": "edit", "source": "Bad", "dest": "Good", "conditions": "input_ok"},
    {"trigger": "edit", "source": "Bad", "dest": "Bad"},
    {"trigger": "edit", "source": "Good", "dest": "Good", "conditions": "input_ok"},
    {"trigger": "edit", "source": "Good", "dest": "Bad"},
    {"trigger": "register", "source": "Good", "dest": "Sent", "conditions": "sent_ok"},
    {"trigger": "register", "source": "Good", "dest": "Good"},
    {"trigger": "modify", "source": "Sent", "dest": "Good"},
    {"trigger": "retry", "source": "Sent", "dest": "Sent"},
    {"trigger": "verify", "source": "Sent", "dest": "Done", "conditions": "code_ok"},
    {"trigger": "verify", "source": "Sent", "dest": "Sent"},
    {"trigger": "disconnect", "source": "*", "dest": "Disconnected"},
)
TRIGGERS = set(transition["trigger"] for transition in TRANSITIONS)
REGISTRATION_FSM = {
    "states": ("Bad", "Good", "Sent", "Done", "Disconnected"),
    "initial": "Bad",
    "transitions": TRANSITIONS,
}
NAMESPACE = "/ruteni/registration"


machines: dict[str, AsyncMachine] = {}


async def on_connect(sid: str, environ: dict[str, str]) -> bool:
    # get the current user
    user = get_user_from_environ(environ)
    if user is not None:
        return False  # the user is connected; reject connection

    # async def emit(*args, **kwargs) -> None:  # type: ignore
    #     await sio.emit(*args, room=sid, **kwargs)

    registration = Registration()
    machines[sid] = AsyncMachine(registration, **REGISTRATION_FSM)
    logger.debug(f"{sid} connected")
    return True


async def on_disconnect(sid: str) -> None:
    await machines[sid].model.disconnect()
    del machines[sid]
    logger.debug(f"{sid} disconnected")


async def catch_all(event: str, sid: str, data: Optional[Any] = None) -> Any:
    logger.debug(event, machines[sid].model.state, data)
    if event not in TRIGGERS:
        return {"error": "unknown-command"}
    rv: list = []
    registration = machines[sid].model
    try:
        if data is None:
            await registration.trigger(event, rv)
        elif isinstance(data, dict):
            await registration.trigger(event, rv, **data)
        elif isinstance(data, list):
            await registration.trigger(event, rv, *data)
        else:
            await registration.trigger(event, rv, data)
    except MachineError:
        return {"error": "unauthorized-command"}
    except TypeError:
        # this exception will be raised if the command parameters are wrong, e.g.:
        #   input_ok() got an unexpected keyword argument 'invalid-display-name'
        # TODO: this exception is too broad
        return {"error": "invalid-arguments"}
    except Exception:
        return {"error": "unexpected-error"}

    logger.debug("rv", rv)
    return tuple(rv)


async def startup(app: Starlette) -> None:
    sio = app.state.sio
    sio.on("connect", on_connect, namespace=NAMESPACE)
    sio.on("disconnect", on_disconnect, namespace=NAMESPACE)
    sio.on("*", catch_all, namespace=NAMESPACE)
    logger.info("started")


async def shutdown(app: Starlette) -> None:
    # @todo unsubscribe if possible one day
    logger.info("stopped")


configuration.add_service("registration", startup, shutdown)

logger.info("loaded")
