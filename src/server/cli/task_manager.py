from typing import Sequence, Type, TypeAlias
import sys
from argparse import ArgumentParser, _SubParsersAction
from threading import Thread
from .interface_command import InterfaceCommand
from .task import Task




ITask: TypeAlias = InterfaceCommand[None]


class TaskManager(InterfaceCommand[Sequence[str]]):
    def __init__(
        self,
        name: str,
        subparser: _SubParsersAction
    ) -> None:
        self.__name: str = name

        self.__argument: ArgumentParser = subparser.add_parser(
            name=name
        )

        self.__tasks: list[Task] = []

    @property
    def name(self) -> str:
        return self.__name

    def add_task(self, task_class: Type[ITask]) -> None:
        t: Task = task_class(self.__argument)

        self.__tasks.append(t)

    def execute(self, arg: Sequence[str]) -> None:
        tasks_found: list[Thread] = [
            Thread(target=task.execute)
            for task in self.__tasks
            if task.name in arg
        ]

        print(self.__tasks[0].name)

        if not tasks_found:
            self.__argument.print_help()

            sys.exit(0)

        [t.start() for t in tasks_found]
        [t.join() for t in tasks_found]