class UrlMaker:
    @staticmethod
    def pg_url(
        pg_user: str, pg_password: str, pg_host: str, pg_port: str, pg_db: str
    ) -> str:
        return f"{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"

    @staticmethod
    def sync_pg_url(
        pg_user: str, pg_password: str, pg_host: str, pg_port: str, pg_db: str
    ) -> str:
        return f"postgresql+psycopg2://{UrlMaker.pg_url(pg_user, pg_password, pg_host, pg_port, pg_db)}"

    @staticmethod
    def async_pg_url(
        pg_user: str, pg_password: str, pg_host: str, pg_port: int, pg_db: str
    ) -> str:
        return f"postgresql+asyncpg://{UrlMaker.pg_url(pg_user, pg_password, pg_host, pg_port, pg_db)}"
