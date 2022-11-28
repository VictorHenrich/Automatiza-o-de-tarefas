from __future__ import annotations
from dataclasses import dataclass
from typing import Union, Optional
from .interface_database import InterfaceDatabase
from .database import Database


@dataclass
class DialectBuilder:
    dialect: str = ""
    name: str = ""
    host: Optional[str] = None
    port: Optional[Union[str, int]] = None
    dbname: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    driver: Optional[str] = None
    driver_async: Optional[str] = None
    async_: bool = False
    debug: bool = False

    def set_name(self, name: str) -> DialectBuilder:
        self.name = name
        
    def set_host(self, host: str) -> DialectBuilder:
        self.host = host

        return self

    def set_port(self, port: Union[str, int]) -> DialectBuilder:
        self.port = port

        return self

    def set_dbname(self, dbname: str) -> DialectBuilder:
        self.dbname = dbname

        return self

    def set_credentials(self, username: str, password: str) -> DialectBuilder:
        self.username = username

        self.password = password

    def set_drives(self, driver_default: str, driver_async: Optional[str]) -> DialectBuilder:
        self.driver = driver_default
        self.driver_async = driver_async

    def set_async(self, async_: bool) -> DialectBuilder:
        self.async_ = async_

        return self

    def set_debug(self, debug: bool) -> DialectBuilder:
        self.debug = debug

        return self

    def build(self) -> InterfaceDatabase:
        driver: str = self.driver if self.async_ else self.driver_async

        url: str =  f"{self.dialect}+{driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.dbname}"

        return Database(
            url,
            self.name,
            self.async_,
            self.debug
        )
    

