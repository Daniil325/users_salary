from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


class DBSession:
    def __init__(self, url, debug: bool = False, readonly: bool = False):
        engine = create_async_engine(
            str(url), echo=debug, pool_pre_ping=True, pool_recycle=3600
        )
        # Not use transaction for read-only connections
        self.engine = (
            engine.execution_options(isolation_level="AUTOCOMMIT")
            if readonly
            else engine
        )
        self.sessionmaker = async_sessionmaker(self.engine, expire_on_commit=False)

    async def close(self):
        await self.engine.dispose()