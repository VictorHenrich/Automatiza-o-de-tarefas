from argparse import ArgumentParser, _SubParsersAction, Namespace
from typing import (
    Tuple,
    Sequence, 
    Type, 
    Mapping, 
    Callable,
    TypeAlias
)
from .interface_command import InterfaceCommand
from .task_manager import TaskManager



IManagerTask: TypeAlias = InterfaceCommand[Sequence[str]]
ITask: TypeAlias = InterfaceCommand[None]



class CliManager(InterfaceCommand[None]):
    def __init__(
        self,
        name: str,
        version: float,
        description: str = "",
        usage: str = ""
    ) -> None:
        argument, subparsers = self.__create_config_argument(
            name,
            description,
            version,
            usage or ""
        )

        self.__argument: ArgumentParser = argument

        self.__subparsers: _SubParsersAction[ArgumentParser] = subparsers

        self.__managers: Mapping[str, IManagerTask] = {}

    def __create_config_argument(
        self,
        program_name: str,
        program_description: str,
        program_version: float,
        program_usage: str
    ) -> Tuple[ArgumentParser, _SubParsersAction]:
        argument: ArgumentParser = ArgumentParser(
            prog=program_name,
            description=program_description,
            usage=program_usage
        )

        subparsers: _SubParsersAction[ArgumentParser] = argument.add_subparsers(
            dest="module",
            description="These modules are the task managers created in the system.",
            title="Task Managers",
            required=True
        )


        argument.add_argument(
            '-v', 
            '--version', 
            action="version", 
            version=f"{program_name} {program_version}"
        )

        return argument, subparsers

    def create_task_manager(self, name: str) -> None:
        manager: IManagerTask = TaskManager(name, self.__subparsers)

        self.__managers[manager.name] = manager

    def add_task(self, module_name: str) -> Callable[[Type[ITask]], Type[ITask]]:
        def wrapper(cls: Type[ITask]) -> Type[ITask]:
            task_manager: TaskManager = [
                manager
                for key, manager in self.__managers.items()
                if key == module_name
            ][0]

            task_manager.add_task(cls)

            return cls

        return wrapper

    def execute(self) -> None:
        namespaces: Namespace = self.__argument.parse_args()

        try:
            task_manager: IManagerTask = [
                manager
                for key, manager in self.__managers.items()
                if key == namespaces.module
            ][0]

        except IndexError:
            self.__argument.print_help()

        else:
            args: Sequence[str] = [
                key
                for key, value in namespaces.__dict__.items()
                if value is True
            ]

            task_manager.execute(args)