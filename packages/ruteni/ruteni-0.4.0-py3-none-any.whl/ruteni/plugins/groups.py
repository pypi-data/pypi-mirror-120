import enum
import logging

from ruteni.plugins.database import database, metadata
from ruteni.plugins.users import users
from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
    and_,
    event,
    func,
    text,
)
from sqlalchemy.engine.base import Connection
from sqlalchemy.sql import select

logger = logging.getLogger(__name__)


class GroupStatus(enum.Enum):
    member = 1
    manager = 2
    owner = 3


groups = Table(
    "groups",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(28), nullable=False),
    Column("added_at", DateTime, nullable=False, server_default=func.now()),
    Column("disabled_at", DateTime, default=None),
)

Index(
    "ix_groups_name_not_disabled",
    groups.c.name,
    unique=True,
    sqlite_where=groups.c.disabled_at.is_(None),
    postgresql_where=groups.c.disabled_at.is_(None),
)

memberships = Table(
    "memberships",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey(users.c.id), nullable=False),
    Column("group_id", Integer, ForeignKey(groups.c.id), nullable=False),
    Column("status", Enum(GroupStatus), nullable=False),
    # Column("added_by", Integer, ForeignKey(users.c.id), nullable=False),
    Column("added_at", DateTime, nullable=False, server_default=func.now()),
    # Column("disabled_by", Integer, ForeignKey(users.c.id), default=None),
    Column("disabled_at", DateTime, default=None),
)

Index(
    "ix_memberships_user_group_not_disabled",
    memberships.c.user_id,
    memberships.c.group_id,
    unique=True,
    sqlite_where=memberships.c.disabled_at.is_(None),
    postgresql_where=memberships.c.disabled_at.is_(None),
)


def after_create(target: Table, connection: Connection, **kwargs):  # type: ignore
    connection.execute(text("INSERT INTO %s (name) VALUES ('admin')" % target.name))


event.listen(groups, "after_create", after_create)


async def get_user_groups(user_id: int) -> list[str]:
    return [
        row["name"]
        for row in await database.fetch_all(
            select([groups.c.name])
            .select_from(groups.join(memberships))
            .where(
                and_(
                    memberships.c.user_id == user_id,
                    users.c.disabled_at.is_(None),
                    groups.c.disabled_at.is_(None),
                    memberships.c.disabled_at.is_(None),
                )
            )
        )
    ]


async def add_user_to_group(
    user_id: int, group_name: str, status: GroupStatus = GroupStatus.member
) -> int:
    # TODO: try to use insert(memberships).from_select(...)
    group_id = await database.fetch_val(
        select([groups.c.id]).where(
            and_(groups.c.name == group_name, groups.c.disabled_at.is_(None))
        )
    )
    if group_id is None:
        raise Exception(f"unknown group {group_name}")

    membership_id = await database.execute(
        memberships.insert().values(user_id=user_id, group_id=group_id, status=status)
    )
    return membership_id


logger.info("loaded")
