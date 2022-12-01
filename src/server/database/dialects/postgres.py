from ..dialect_builder import DialectBuilder



class Postgres(DialectBuilder):
    def __init__(self) -> None:
        super().__init__(
            dialect="postgresql",
            port=5432,
            driver="psycopg2",
            driver_async="asyncpg"
        )