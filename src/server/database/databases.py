from typing import (
    Mapping,
    Optional,
    Mapping,
    Union,
    Any,
    List
)
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from .database import Database
from .interface_database import InterfaceDatabase
from .dialect_builder import DialectBuilder
from .dialects import (
    MySQL,
    Postgres
)




class Databases:
    dialects: List[DialectBuilder] = [
        MySQL(),
        Postgres()
    ]

    def __init__(self) -> None:
        self.__bases: Mapping[str, InterfaceDatabase] = {}

    @property
    def bases(self) -> Mapping[str, InterfaceDatabase]:
        return self.__bases

    def add_database(self, database: Database) -> None:
        self.__bases[database.name] = database

    def get_database(self, name: Optional[str] = None) -> InterfaceDatabase:
        if len(self.__bases) == 1 and not name:
            return list(self.__bases.values)[0]

        else:
            return self.__bases[name]

    def create_session(
        self,
        database_name: Optional[str] = None,
        **options: Mapping[str, Any]
    ) -> Union[Session, AsyncSession]:
        database: InterfaceDatabase = self.get_database(database_name)

        return database.create_session(**options)

    def migrate(
        self,
        database_name: Optional[str] = None,
        drop_tables: bool = False,
        **options: Mapping[str, Any]
    ) -> None:
        database: InterfaceDatabase = self.get_database(database_name)

        database.migrate(drop_tables, **options)
