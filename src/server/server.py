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


Target: TypeAlias = Callable[[None], None]


class Server:
    def __init__(
        self,
        cli: CliManager
    ) -> None:
        self.__cli: CliManager = cli
        self.__listeners: List[Target] = []

    @property
    def cli(self) -> CliManager:
        return self.__cli

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
    def __create_cli(cls, data: Mapping[str, Any]) -> CliManager:
        managers: Sequence[str] = data['managers']

        del data['managers']

        cli: CliManager = CliManager(**data)

        for manager_name in managers:
            cli.create_task_manager(manager_name)

        return cli

    @classmethod
    def create(
        cls,
        cli: Mapping[str, Any]
    ) -> Server:
        cli_manager: CliManager = cls.__create_cli(cli)

        return Server(cli_manager)