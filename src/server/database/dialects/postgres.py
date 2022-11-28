from ..dialect_builder import DialectBuilder



class Postgres(DialectBuilder):
    def __init__(self, name: str) -> None:
        super().__init__(
            name=name,
            dialect="postgresql",
            port=5432,
            driver="psycopg2",
            driver_async="asyncpg"
        )