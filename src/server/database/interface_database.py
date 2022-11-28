from typing import (
    Protocol,
    Sequence,
    Mapping,
    Any,
    TypeAlias,
    Union
)
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession


Args: TypeAlias = Sequence[Any]
Kwargs: TypeAlias = Mapping[str, Any]



class InterfaceDatabase(Protocol):
    def create_session(
        self, 
        *args: Args, 
        **kwargs: Kwargs
    ) -> Union[Session, AsyncSession]:
        pass

    def migrate(
        self, 
        drop_tables: bool = False, 
        *args: Args,
        **kwargs: Kwargs
    ) -> None:
        pass