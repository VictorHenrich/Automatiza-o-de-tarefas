from .config import (
    OPTIONS_CLI,
    OPTIONS_DATABASES
)
from server import ServerFactory, Server



app: Server = ServerFactory.create(
    OPTIONS_CLI,
    OPTIONS_DATABASES
)