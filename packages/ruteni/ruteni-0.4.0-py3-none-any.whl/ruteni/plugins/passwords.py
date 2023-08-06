import logging
from typing import NamedTuple, Optional

import bcrypt
from ruteni import configuration
from ruteni.plugins.database import database, metadata
from ruteni.plugins.users import users, add_user
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
    and_,
    func,
)
from sqlalchemy.sql import select

# from passlib.hash import bcrypt

logger = logging.getLogger(__name__)

PASSWORD_MAX_LENGTH: int = configuration.get(
    "RUTENI_PASSWORD_MAX_LENGTH", cast=int, default=40
)

passwords = Table(
    "passwords",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey(users.c.id), nullable=False),
    Column("hashed_password", String(60), nullable=False),  # TODO: length as pref?
    Column("added_at", DateTime, nullable=False, server_default=func.now()),
    Column("disabled_at", DateTime, default=None),
)


Index(
    "ix_passwords_user_id_not_disabled",
    passwords.c.user_id,
    unique=True,
    sqlite_where=passwords.c.disabled_at.is_(None),
    postgresql_where=passwords.c.disabled_at.is_(None),
)


class PasswordInfo(NamedTuple):
    user_id: int
    hashed_password: str


def hash_password(password: str) -> str:
    "Hash a password"
    salt = bcrypt.gensalt(rounds=6, prefix=b"2a")
    return bcrypt.hashpw(password.encode(), salt).decode()


def verify_password(password: str, hashed_password: str) -> bool:
    b_hashed_password = hashed_password.encode()
    return bcrypt.hashpw(password.encode(), b_hashed_password) == b_hashed_password


async def get_password(email: str) -> Optional[PasswordInfo]:
    row = await database.fetch_one(
        select([users.c.id, passwords.c.hashed_password])
        .select_from(users.join(passwords))
        .where(
            and_(
                users.c.email == email,
                users.c.disabled_at.is_(None),
                passwords.c.disabled_at.is_(None),
            )
        )
    )
    return PasswordInfo(row["id"], row["hashed_password"]) if row else None


async def check_password(email: str, password: str) -> Optional[PasswordInfo]:
    info = await get_password(email)
    if info is not None:
        logger.debug("signin:", email, password, "~", info.hashed_password)
        if verify_password(password, info.hashed_password):
            return info
    return None


async def add_password(user_id: int, password: str) -> int:
    # hashed_password = bcrypt.hash(self.password)
    hashed_password = hash_password(password)
    return await database.execute(
        passwords.insert().values(user_id=user_id, hashed_password=hashed_password)
    )


async def register_user(
    display_name: str, email: str, locale: str, password: str
) -> tuple[int, int]:
    user_info = await add_user(display_name, email, locale)
    password_id = await add_password(user_info.id, password)
    return user_info.id, password_id


logger.info("loaded")
