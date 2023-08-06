import logging

from ruteni import configuration
from ruteni.plugins.database import database, metadata
from ruteni.plugins.session import get_user_from_environ
from ruteni.plugins.users import users
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, func
from sqlalchemy_utils import IPAddressType
from starlette.applications import Starlette

logger = logging.getLogger(__name__)

connections = Table(
    "connections",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("sid", String(28), nullable=False),
    Column("ip_address", IPAddressType, nullable=False),
    Column("user_id", Integer, ForeignKey(users.c.id), nullable=False),
    Column("opened_at", DateTime, nullable=False, server_default=func.now()),
    Column("closed_at", DateTime, default=None),
)


async def on_connect(sid: str, environ: dict[str, str]) -> bool:
    # async with self.app.state.sio.eio.session(sid) as session:
    #     session["username"] = username

    # get the current user
    user = get_user_from_environ(environ)
    if user is None:
        return False  # reject connection

    query = connections.insert().values(
        sid=sid, user_id=user["id"], ip_address=environ["REMOTE_ADDR"]
    )
    await database.execute(query)
    logger.info(f"{user['name']} is connected")
    return True


async def on_disconnect(sid: str) -> None:
    await database.execute(
        connections.update()
        .where(connections.c.sid == sid)
        .values(closed_at=func.now())
    )
    logger.info(f"{sid}.disconnect")


async def startup(app: Starlette) -> None:
    app.state.sio.on("connect", on_connect)
    app.state.sio.on("disconnect", on_disconnect)
    logger.info("started")


async def shutdown(app: Starlette) -> None:
    # @todo unsubscribe if possible one day
    logger.info("stopped")


configuration.add_service("presence", startup, shutdown)

logger.info("loaded")
