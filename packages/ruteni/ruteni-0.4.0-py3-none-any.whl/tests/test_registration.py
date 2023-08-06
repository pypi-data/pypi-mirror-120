#!/usr/bin/python3 -W ignore::DeprecationWarning

from datetime import datetime
from html.parser import HTMLParser
from typing import Any
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

import aiohttp
import socketio
from ruteni import Ruteni

# must be imported before plugins
from .config import (
    CLIENT_ID,
    DATABASE_PATH,
    DOMAIN,
    USER_EMAIL,
    USER_LOCALE,
    USER_NAME,
    USER_PASSWORD,
)

from ruteni.plugins.jwkeys import jwkeys
from ruteni.plugins.registration import SITE_NAME
from ruteni.plugins.token import (
    ACCESS_TOKEN_EXPIRATION,
    REFRESH_TOKEN_EXPIRATION,
    new_refresh_token,
)
from ruteni.plugins.token_auth import ACCESS_TOKEN_COOKIE_NAME
from starlette import status
from starlette.middleware.cors import ALL_METHODS


from .server import UvicornTestServer
from .dns import DNSMock
from .smtp import SMTPMock

BASE_URL = "http://localhost:8000"
NAMESPACE = "/ruteni/registration"
OPTIONS = dict(transports=["websocket"], namespaces=NAMESPACE)
MX_SERVER = "mx." + DOMAIN
SIGNIN_URL = BASE_URL + "/api/jauthn/v1/signin"
SIGNOUT_URL = BASE_URL + "/api/jauthn/v1/signout"
USER = {
    "id": 2,
    "display_name": USER_NAME,
    "email": USER_EMAIL,
    "locale": USER_LOCALE,
}


class VerificationEmailHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_a = False
        self.code: str = ""

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if self.code == "":
            self.in_a = tag == "a"

    def handle_endtag(self, tag: str) -> None:
        if self.code == "":
            self.in_a = False

    def handle_data(self, data: str) -> None:
        if self.code == "" and self.in_a and len(data) == 6:
            self.code = data


class JAuthNTestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.server = UvicornTestServer(Ruteni())
        await self.server.up()
        self.sio = socketio.AsyncClient(reconnection=False)
        await self.sio.connect(BASE_URL, **OPTIONS)

    async def asyncTearDown(self) -> None:
        await self.sio.disconnect()
        await self.sio.eio.http.close()  # TODO: socketio bug?
        await self.server.down()

    def tearDown(self) -> None:
        # self.test_dir.cleanup()
        # self.test_dir.close()
        pass

    def valid_signin_info(self, content: dict[str, Any]) -> bool:
        return (
            "access_token" in content
            and "refresh_token" in content
            and "user" in content
        )

    async def call(self, *args, **kwargs) -> Any:  # type: ignore
        return await self.sio.call(*args, namespace=NAMESPACE, **kwargs)

    async def emit_edit(
        self, display_name: str, email: str, password: str, locale: str
    ) -> dict:
        return await self.call(
            "edit",
            {
                "display_name": display_name,
                "email": email,
                "password": password,
                "locale": locale,
            },
        )

    async def test_0_register(self) -> None:
        # send a bogus event
        self.assertEqual(await self.call("unknown"), {"error": "unknown-command"})

        # send bogus arguments
        self.assertEqual(await self.call("edit", None), {"error": "invalid-arguments"})
        self.assertEqual(await self.call("edit", 42), {"error": "invalid-arguments"})
        self.assertEqual(await self.call("edit", "a"), {"error": "invalid-arguments"})
        self.assertEqual(await self.call("edit", []), {"error": "invalid-arguments"})
        self.assertEqual(await self.call("edit", {}), {"error": "invalid-arguments"})
        self.assertEqual(
            await self.call("edit", {"email": ""}), {"error": "invalid-arguments"}
        )
        self.assertEqual(
            await self.call("edit", {"bogus-param": ""}), {"error": "invalid-arguments"}
        )

        self.assertEqual(
            await self.emit_edit("", "", "", ""),
            {
                "invalid-display-name": "empty",
                "invalid-email": "empty",
                "invalid-password": "empty",
                "invalid-locale": "empty",
            },
        )
        self.assertEqual(
            await self.emit_edit(100 * "x", 100 * "x", 100 * "x", ""),
            {
                "invalid-display-name": "overflow",
                "invalid-email": "overflow",
                "invalid-password": "overflow",
                "invalid-locale": "empty",
            },
        )
        self.assertEqual(
            await self.emit_edit(USER_NAME, "incomplete-email", "", "fr-FR"),
            {"invalid-email": "incomplete", "invalid-password": "empty"},
        )
        self.assertEqual(
            await self.emit_edit(USER_NAME, "foo@", "", "en-US"),
            {"invalid-email": "incomplete", "invalid-password": "empty"},
        )
        self.assertEqual(
            await self.emit_edit(USER_NAME, "fooé@", "", "de-DE"),
            {
                "invalid-email": "parse-error",
                "invalid-password": "empty",
                "invalid-locale": "unknown",
            },
        )
        self.assertEqual(
            await self.emit_edit(USER_NAME, "@", "", "fr-FR"),
            {"invalid-email": "parse-error", "invalid-password": "empty"},
        )
        self.assertEqual(
            await self.emit_edit(USER_NAME, "@fr", "", "fr-FR"),
            {"invalid-email": "parse-error", "invalid-password": "empty"},
        )
        self.assertEqual(
            await self.emit_edit(USER_NAME, "foo@@", "bad", "fr-FR"),
            {"invalid-email": "parse-error", "low-password-strength": 0},
        )
        self.assertEqual(
            await self.emit_edit(USER_NAME, "é@bar", "littlebetter", "fr-FR"),
            {"invalid-email": "parse-error", "low-password-strength": 1},
        )

        dns = DNSMock({DOMAIN: [(MX_SERVER, 1, 1)]})
        with patch(
            "ruteni.plugins.registration.query_mx",
            wraps=dns.query_mx,
        ):
            self.assertEqual(
                await self.emit_edit(USER_NAME, "foo@é", "0xbar45", "fr-FR"),
                {"invalid-email": "unknown-domain", "low-password-strength": 2},
            )

        with patch(
            "ruteni.plugins.registration.query_mx",
            wraps=dns.query_mx,
        ):
            self.assertEqual(
                await self.emit_edit(USER_NAME, USER_EMAIL, USER_PASSWORD, "fr-FR"),
                {},
            )

        # now that the fields are okay, register using a mock SMTP function
        smtp = SMTPMock()
        with patch(
            "ruteni.plugins.registration.send_mail",
            wraps=smtp.send_mail,
        ):
            self.assertTrue(await self.call("register"))

        # send a wrong verification code
        self.assertFalse(await self.call("verify", "xxxxxx"))

        # get the email that was sent, extract the code and send it
        message = smtp.get_email(MX_SERVER)
        html = message.get_payload()
        parser = VerificationEmailHTMLParser()
        parser.feed(html)
        self.assertTrue(await self.call("verify", parser.code))

        # send a known event but in the wrong state
        self.assertEqual(await self.call("edit"), {"error": "unauthorized-command"})

        # test signin
        # async def test_1_signin(self) -> None:
        async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar()) as session:

            # only POST allowed
            for method in ALL_METHODS:
                if method != "POST":
                    async with session.request(method, SIGNIN_URL) as response:
                        self.assertEqual(
                            response.status, status.HTTP_405_METHOD_NOT_ALLOWED
                        )

            async with session.post(SIGNIN_URL, data=b"data") as response:
                self.assertEqual(
                    response.status, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
                )

            # json content type but bad with content
            async with session.post(
                SIGNIN_URL,
                data=b"{",
                headers={"Content-Type": "application/json"},
            ) as response:
                self.assertEqual(response.status, status.HTTP_422_UNPROCESSABLE_ENTITY)

            # multipart content type but with bad content
            async with session.post(
                SIGNIN_URL,
                data=b"{",
                headers={"Content-Type": "multipart/form-data"},
            ) as response:
                self.assertEqual(response.status, status.HTTP_422_UNPROCESSABLE_ENTITY)

            # send json without any field
            async with session.post(SIGNIN_URL, json={}) as response:
                self.assertEqual(response.status, status.HTTP_400_BAD_REQUEST)

            # send form without any field
            data = aiohttp.formdata.FormData()
            async with session.post(SIGNIN_URL, data=data) as response:
                self.assertEqual(response.status, status.HTTP_400_BAD_REQUEST)

            # send json with email and password but a third parameter
            async with session.post(
                SIGNIN_URL, json={"email": "", "password": "", "foo": ""}
            ) as response:
                self.assertEqual(response.status, status.HTTP_400_BAD_REQUEST)

            # send form with email and password but a third parameter
            data = aiohttp.formdata.FormData()
            data.add_field("email", "")  # , content_type="application/json")
            data.add_field("password", "")
            data.add_field("foo", "")
            async with session.post(SIGNIN_URL, data=data) as response:
                self.assertEqual(response.status, status.HTTP_400_BAD_REQUEST)

            # send json with email and password but not all strings
            async with session.post(
                SIGNIN_URL,
                json={"email": 1, "password": "", "client_id": 1},
            ) as response:
                self.assertEqual(response.status, status.HTTP_400_BAD_REQUEST)

            # send form with all fields but wrongs ones
            data = aiohttp.formdata.FormData()
            data.add_field("email", "qux@foo.fr")  # , content_type="application/json")
            data.add_field("password", "baz")
            data.add_field("client_id", CLIENT_ID)
            async with session.post(SIGNIN_URL, data=data) as response:
                self.assertEqual(response.status, status.HTTP_401_UNAUTHORIZED)

            # send json with email and password but wrongs ones
            async with session.post(
                SIGNIN_URL,
                json={
                    "email": "qux@foo.fr",
                    "password": "baz",
                    "client_id": CLIENT_ID,
                },
            ) as response:
                self.assertEqual(response.status, status.HTTP_401_UNAUTHORIZED)

            # send form with correct email but wrong password
            data = aiohttp.formdata.FormData()
            data.add_field("email", USER_EMAIL)
            data.add_field("password", "bad-password")
            data.add_field("client_id", CLIENT_ID)
            async with session.post(SIGNIN_URL, data=data) as response:
                self.assertEqual(response.status, status.HTTP_401_UNAUTHORIZED)

            # send json with correct email but wrong password
            async with session.post(
                SIGNIN_URL,
                json={
                    "email": USER_EMAIL,
                    "password": "bad-password",
                    "client_id": CLIENT_ID,
                },
            ) as response:
                self.assertEqual(response.status, status.HTTP_401_UNAUTHORIZED)

            now = int(datetime.now().timestamp())
            COMMOM_CLAIMS = {
                "sub": "2",
                "iat": now,
                "exp": now + ACCESS_TOKEN_EXPIRATION,
                "rte": now + REFRESH_TOKEN_EXPIRATION,
                "orig_iat": 0,
                "iss": SITE_NAME,
                "email": USER_EMAIL,
                "display_name": USER_NAME,
                "scope": [],
                "client_id": CLIENT_ID,
            }

            # send form with correct email and password as form
            refresh_token = new_refresh_token()
            with patch(
                "ruteni.plugins.token.now", wraps=lambda: datetime.fromtimestamp(now)
            ), patch(
                "ruteni.plugins.token.new_refresh_token",
                wraps=lambda: refresh_token,
            ):
                data = aiohttp.formdata.FormData()
                data.add_field("email", USER_EMAIL)
                data.add_field("password", USER_PASSWORD)
                data.add_field("client_id", CLIENT_ID)
                async with session.post(SIGNIN_URL, data=data) as response:
                    self.assertEqual(response.status, status.HTTP_200_OK)
                    content = await response.json()
                    self.assertEqual(
                        content,
                        {
                            "access_token": {"jti": "1", **COMMOM_CLAIMS},
                            "refresh_token": refresh_token,
                            "user": USER,
                        },
                    )
                    self.assertTrue(self.valid_signin_info(content))

            # send json with correct email and password as json
            # because refresh tokens must be unique, use a new one
            refresh_token = new_refresh_token()
            with patch(
                "ruteni.plugins.token.now", wraps=lambda: datetime.fromtimestamp(now)
            ), patch(
                "ruteni.plugins.token.new_refresh_token",
                wraps=lambda: refresh_token,
            ):
                async with session.post(
                    SIGNIN_URL,
                    json={
                        "email": USER_EMAIL,
                        "password": USER_PASSWORD,
                        "client_id": CLIENT_ID,
                    },
                ) as response:
                    self.assertEqual(response.status, status.HTTP_200_OK)
                    content = await response.json()
                    self.assertEqual(
                        content,
                        {
                            "access_token": {"jti": "2", **COMMOM_CLAIMS},
                            "refresh_token": refresh_token,
                            "user": USER,
                        },
                    )
                    self.assertEqual(len(session.cookie_jar), 1)
                    cookie = next(session.cookie_jar.__iter__())
                    self.assertEqual(cookie.key, ACCESS_TOKEN_COOKIE_NAME)
                    access_token = cookie.value
                    self.assertEqual(
                        jwkeys.decrypt(access_token), {"jti": "2", **COMMOM_CLAIMS}
                    )

            # only POST allowed for signout
            for method in ALL_METHODS:
                if method != "POST":
                    async with session.request(method, SIGNOUT_URL) as response:
                        self.assertEqual(
                            response.status, status.HTTP_405_METHOD_NOT_ALLOWED
                        )

            async with session.post(
                SIGNOUT_URL,
                json={"refresh_token": refresh_token},
            ) as response:
                self.assertEqual(response.status, status.HTTP_200_OK)


if __name__ == "__main__":
    import unittest

    unittest.main()
