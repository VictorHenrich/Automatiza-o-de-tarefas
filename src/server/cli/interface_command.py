from typing import (
    Protocol, 
    Generic,
    TypeVar,
    Optional
)


T = TypeVar('T')


class InterfaceCommand(Protocol, Generic[T]):
    def execute(self, arg: Optional[T]) -> None:
        pass