from abc import ABC, abstractmethod
from typing import Optional, List
from argparse import ArgumentParser
from .interface_command import InterfaceCommand
from .impression_task import ImpressionTask

        
class Task(ABC, InterfaceCommand[None]):

    name: str = ""
    title: str = ""
    subtitle: Optional[str] = None
    shortname: Optional[str] = None
    description: Optional[str] = None
    debug: bool = False

    def __init__(self, parser: ArgumentParser) -> None:
        if not self.__class__.name:
            raise Exception(f"name parameter required not defined in class {self.__class__.__name__}!")

        if not self.__class__.title:
            raise Exception(f"title parameter required not defined in class {self.__class__.__name__}!")

        self.__add_argument(parser)

    @property
    def name(self) -> str:
        return self.__class__.name
        
    @abstractmethod
    def run(self) -> None:
        pass

    def __add_argument(
        self,
        parser: ArgumentParser
    ) -> None:
        flags: List = [f"--{self.__class__.name}"]

        if(self.__class__.shortname):
            flags.insert(0, f"-{self.__class__.shortname}")

        parser.add_argument(
            *flags,
            action="store_true",
            help=self.__class__.description
        )

    def execute(self) -> None:
        impression: ImpressionTask = ImpressionTask(
            self.__class__.title,
            self.__class__.subtitle,
            self.__class__.debug
        )

        impression.print(self.run)
