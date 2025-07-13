from src.application.usecases import GetSalaryCommand, LoginCommand, RegisterUserCommand
from src.infra.auth.jwt import JWTService, PasswordManager
from src.infra.database.repo import SalaryScheduleRepo, UserRepo
from src.infra.database.session import DBSession
from src.infra.redis import RedisImpl
from src.settings import AuthJWTSettings, Settings
from src.utils import UrlMaker
from src.infra.database.mapping import mapper_registry  # noqa

from redis.asyncio import Redis


def get_settings():
    return Settings()


def get_jwt_settings():
    return AuthJWTSettings()


def get_pg_url():
    app_settings = get_settings()
    return UrlMaker.async_pg_url(
        app_settings.POSTGRES_USER,
        app_settings.POSTGRES_PASSWORD,
        app_settings.POSTGRES_HOST,
        app_settings.POSTGRES_PORT,
        app_settings.POSTGRES_DB,
    )


async def get_db_session():
    db_session = DBSession(get_pg_url())
    async with db_session.sessionmaker() as session:
        yield session
        await session.aclose()
        
        
async def get_salary_schedule_repo():
    return SalaryScheduleRepo(await anext(get_db_session()))


async def get_user_repo():
    return UserRepo(await anext(get_db_session()))


def get_redis_repo():
    app_settings = get_settings()
    redis = Redis.from_url(app_settings.REDIS_URL)
    return RedisImpl(redis)


def get_jwt_service() -> JWTService:
    return JWTService(get_jwt_settings())


async def get_salary_command():
    return GetSalaryCommand(get_redis_repo(), await get_salary_schedule_repo())


async def get_login_command():
    return LoginCommand(await get_user_repo(), PasswordManager())


async def get_register_user_command():
    return RegisterUserCommand(await get_user_repo(), PasswordManager())

