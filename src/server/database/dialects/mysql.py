from ..dialect_builder import DialectBuilder



class MySQL(DialectBuilder):
    def __init__(self, name: str) -> None:
        super().__init__(
            name=name,
            dialect="mysql",
            port=3306,
            driver="pymysql",
            driver_async="asyncmy"
        )