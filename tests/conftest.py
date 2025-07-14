from redis.asyncio import Redis
from src.infra.database.mapping import mapper_registry

import pytest
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def pytest_addoption(parser):
    parser.addini("redis_uri", "URI for test redis instance")
    parser.addini("pg_uri", "URI for test pg instance")


@pytest.fixture
async def redis(request):
    redis_instance = Redis.from_url(request.config.getini("redis_uri"))
    await redis_instance.flushall()
    return redis_instance


async def create_database(url):
    url_object = make_url(url)
    database_name = url_object.database
    dbms_url = url_object.set(database="")
    engine = create_async_engine(dbms_url, isolation_level="AUTOCOMMIT")

    async with engine.connect() as conn:
        c = await conn.execute(text(f"SHOW DATABASES LIKE '{database_name}';"))
        database_exists = c.scalar() == database_name

    if database_exists:
        await drop_database(url_object)

    async with engine.connect() as conn:
        await conn.execute(text(f"CREATE DATABASE `{database_name}`;"))
    await engine.dispose()


async def drop_database(url):
    url_object = make_url(url)
    dbms_url = url_object.set(database="")
    engine = create_async_engine(dbms_url, isolation_level="AUTOCOMMIT")
    async with engine.connect() as conn:
        await conn.execute(text(f"DROP DATABASE `{url_object.database}`;"))
    await engine.dispose()


@pytest.fixture(scope="function")
async def scoped_sqla_engine(request) -> AsyncEngine:
    url_object = make_url(request.config.getini("mysql_uri"))
    scoped_sqla_url = url_object.set(database=url_object.database + "_function_scoped")
    await create_database(scoped_sqla_url)

    engine = create_async_engine(scoped_sqla_url, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)
    try:
        yield engine
    finally:
        await engine.dispose()
        await drop_database(scoped_sqla_url)


@pytest.fixture(scope="function")
async def database_session(scoped_sqla_engine) -> async_sessionmaker:
    return async_sessionmaker(
        scoped_sqla_engine, expire_on_commit=False, class_=AsyncSession, autoflush=False
    )
