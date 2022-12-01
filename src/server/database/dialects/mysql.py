from ..dialect_builder import DialectBuilder



class MySQL(DialectBuilder):
    def __init__(self) -> None:
        super().__init__(
            dialect="mysql",
            port=3306,
            driver="pymysql",
            driver_async="asyncmy"
        )