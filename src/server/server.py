from typing import (
    Mapping, 
    Any, 
    Sequence, 
    Callable,
    TypeAlias,
    List,
    Coroutine,
    Optional
)
import asyncio
from .cli import CliManager
from .database import Databases, Database, DialectBuilder


Target: TypeAlias = Callable[[None], None]
MappedData: TypeAlias = Mapping[str, Any]




class Server:
    def __init__(
        self,
        cli: CliManager,
        databases: Databases
    ) -> None:
        self.__cli: CliManager = cli

        self.__databases: Databases = databases

        self.__listeners: List[Target] = []

    @property
    def cli(self) -> CliManager:
        return self.__cli

    @property
    def databases(self) -> Databases:
        return self.__databases

    def initialize(self, target: Target) -> Target:
        self.__listeners.append(target)

        return target

    def start(self) -> None:
        for target in self.__listeners:
            result: Optional[Coroutine] = target()

            if isinstance(result, Coroutine):
                asyncio.run(result)



class ServerFactory:

    @classmethod
    def __create_cli(cls, data: MappedData) -> CliManager:
        managers: Sequence[str] = data['managers']

        del data['managers']

        cli: CliManager = CliManager(**data)

        for manager_name in managers:
            cli.create_task_manager(manager_name)

        return cli

    @classmethod
    def __create_databases(cls, data: MappedData) -> Databases:
        databases: Databases = Databases()

        for name, options in data.values():
            database_builder: DialectBuilder

            try:
                database_builder, = [
                    base
                    for base in cls.__dialects__
                    if (options.get('dialect') or '').upper() == base.dialect
                ]

            except ValueError:
                database_builder = DialectBuilder()


            database_builder\
                .set_name(name)\
                .set_host(options['host'])\
                .set_port(options['port'])\
                .set_dbname(options['dbname'])\
                .set_credentials(options['username'], options['password'])\
                

            if options.get('driver') or options.get('driver_async'):
                database_builder\
                    .set_drives(options['driver'], options.get('driver_async'))

            if options.get('async'):
                database_builder.set_async(options.get('async'))

            if options.get('debug'):
                database_builder.set_debug(options.get('debug'))

            database: Database = database_builder.build()

            databases.add_database(database)

    @classmethod
    def create(
        cls,
        cli: MappedData,
        databases: MappedData
    ) -> Server:
        cli_manager: CliManager = cls.__create_cli(cli)

        databases_: Databases = cls.__create_databases(databases)

        return Server(
            cli_manager, 
            databases_
        )