from types import TracebackType
from typing import Optional, Type, TypedDict

import sqlalchemy as sa
from sqlalchemy import engine, orm

from wilddog import config


class SessionFactoryDict(TypedDict, total=False):
    class_type: orm.sessionmaker
    engine: engine.Engine


SessionFactory: SessionFactoryDict = {}

__all__ = ["Session", "sql_engine"]


def sql_engine() -> engine.Engine:
    # init factory
    _session_factory()
    return SessionFactory["engine"]


def _session_factory() -> orm.Session:
    if not SessionFactory:
        postgres_uri = config.wild_dog.database["url"]
        sql_eng = sa.create_engine(postgres_uri, isolation_level="REPEATABLE READ")
        SessionFactory["class_type"] = orm.sessionmaker(
            autocommit=False, autoflush=False, bind=sql_eng
        )
        SessionFactory["engine"] = sql_eng
    return SessionFactory["class_type"]()


class Session:
    def __enter__(self) -> orm.Session:
        self.sxn = _session_factory()
        return self.sxn

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_val: Optional[BaseException] = None,
        exc_tb: Optional[TracebackType] = None,
    ) -> None:
        """Tries to commit amd close provided session. Rolls backs changes if an exception occurs"""
        try:
            self.sxn.commit()
        except Exception as e:
            self.sxn.rollback()
            raise e
        finally:
            self.sxn.close()
