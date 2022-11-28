from .config import (
    OPTIONS_CLI
)
from server import ServerFactory, Server



app: Server = ServerFactory.create(
    OPTIONS_CLI
)