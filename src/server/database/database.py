from typing import (
    Union,
    Type,
    Mapping,
    Any,
    Coroutine
)
import asyncio
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm.decl_api import declarative_base, DeclarativeMeta
from sqlalchemy.orm.session import Session, sessionmaker




class Database:
    def __init__(
        self,
        url: str,
        name: str,
        async_: bool = False,
        debug: bool = False
    ) -> None:
        self.__engine: Union[Engine, AsyncEngine] = self.__create_engine(
            url,
            async_,
            debug
        )

        self.__name: str = name

        self.__Model = declarative_base(self.__engine)

    @property
    def engine(self) -> Union[Engine, AsyncEngine]:
        return self.__engine

    @property
    def Model(self) -> Type[DeclarativeMeta]:
        return self.__Model

    @property
    def name(self) -> str:
        return self.__name

    def __create_default_engine(self, url: str, debug: bool) -> Engine:
        return create_engine(url, echo=debug)

    def __create_async_engine(self, url: str, debug: bool) -> AsyncEngine:
        return create_async_engine(url, echo=debug)

    def __create_engine(
        self,
        url: str,
        async_: bool, 
        debug: bool
    ) -> Union[Engine, AsyncEngine]:
        if not async_:
            return self.__create_default_engine(url, debug)

        else:
            return self.__create_async_engine(url, debug)

    def __migrate_default(self, drop_tables: bool) -> None:
        if drop_tables:
            self.__Model.metadata.drop_all(self.__engine)

        self.__Model.metadata.create_all(self.__engine)

    async def __migrate_async(self, drop_tables: bool) -> Coroutine:
        async with self.__engine.begin() as connection:
            if drop_tables:
                connection.run_async(self.__Model.metadata.drop_all)

            connection.run_async(self.__Model.metadata.create_all)

    def create_session(self, **options: Mapping[str, Any]) -> Union[Session, AsyncSession]:
        return sessionmaker(
            self.__engine,
            class_=Session if type(self.__engine) is Engine else AsyncEngine,
            **options
        )

    def migrate(self, drop_tables: bool = False) -> None:
        if type(self.__engine) is Engine:
            self.__migrate_default(drop_tables)

        else:
            coroutine: Coroutine = self.__migrate_async(drop_tables)

            asyncio.run(coroutine)