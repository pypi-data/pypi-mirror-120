import base64
from datetime import datetime
from typing import Any, Dict, Type

import attr
import sqlalchemy as sa
from sqlalchemy import orm


@attr.s(auto_attribs=True)
class SearchMeta:
    cursor: str


@orm.as_declarative()
class BaseEntity:
    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    date_created: datetime = sa.Column(
        sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")
    )
    last_updated: datetime = sa.Column(
        sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")
    )

    def meta(self) -> SearchMeta:
        enc = base64.b64encode(f"{self.id}-{self.__tablename__}".encode())
        return SearchMeta(cursor=enc.decode())

    def decode_cursor(self, cursor: str) -> int:
        if cursor is None:
            return 0
        dec = base64.b64decode(cursor)
        _id, table_name = dec.split(b"-")
        if table_name != self.__tablename__:
            raise ValueError(f"Unknown id: {cursor} specified")
        return int(_id)

    @orm.declared_attr
    def __tablename__(cls) -> orm.Mapped[str]:  # ignore
        return cls.__name__.lower()
