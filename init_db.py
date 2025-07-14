from datetime import datetime
from src.domain.models import Role, SalarySchedule
import asyncio
from src.infra.database.mapping import mapper_registry, UserInDb
from src.infra.database.session import DBSession
from src.infra.auth.jwt import PasswordManager

from sqlalchemy import insert, text

from src.settings import Settings
from src.utils import UrlMaker

p_m = PasswordManager()


role_1 = insert(Role).values(id="d651b12c-8f02-40cc-b5ec-88fa04019d2b", name="user")
role_2 = insert(Role).values(id="317ad78f-8259-4b7a-a255-8588fd56662e", name="admin")

user_1 = insert(UserInDb).values(
    id="985cbe45-30a7-44a0-a03a-fbbaf43366ad",
    name="Ivan",
    surname="Ivanov",
    username="IvanI",
    salary=100000,
    password=p_m.hash_password("password"),
    role_id="d651b12c-8f02-40cc-b5ec-88fa04019d2b",
)

user_2 = insert(UserInDb).values(
    id="0fb630d1-7694-4256-b6eb-4c704205ac20",
    name="Alex",
    surname="Sidorov",
    username="AlexS",
    salary=150000,
    password=p_m.hash_password("string"),
    role_id="d651b12c-8f02-40cc-b5ec-88fa04019d2b",
)

s_1 = insert(SalarySchedule).values(
    id="0d6430df-4123-4c80-95e3-652030b56f5f",
    user_id="985cbe45-30a7-44a0-a03a-fbbaf43366ad",
    next_date=datetime(2025, 11, 1),
)

s_2 = insert(SalarySchedule).values(
    id="5669ff4e-ee8b-43bb-bf31-c5c546b5f986",
    user_id="0fb630d1-7694-4256-b6eb-4c704205ac20",
    next_date=datetime(2025, 10, 1),
)

app_settings = Settings()


def get_url() -> str:
    return UrlMaker.async_pg_url(
        app_settings.POSTGRES_USER,
        app_settings.POSTGRES_PASSWORD,
        app_settings.POSTGRES_HOST,
        app_settings.POSTGRES_PORT,
        app_settings.POSTGRES_DB,
    )


db_session = DBSession(get_url())


async def insert_data():
    async with db_session.sessionmaker() as session:
        c_roles = await session.execute(
            text(
                f"SELECT EXISTS( SELECT * FROM role limit 1) as has_data;"
            )
        )
        c_users = await session.execute(
            text(
                f"SELECT EXISTS( SELECT * FROM users limit 1) as has_data;"
            )
        )
        c_salary = await session.execute(
            text(
                f"SELECT EXISTS( SELECT * FROM salary_schedule limit 1) as has_data;"
            )
        )
        
        if not c_roles.scalar_one_or_none():
            await session.execute(role_1)
            await session.execute(role_2)
            
        if not c_users.scalar_one_or_none():
            await session.execute(user_1)
            await session.execute(user_2)
            
        if not c_salary.scalar_one_or_none():
            await session.execute(s_1)
            await session.execute(s_2)

    
        await session.commit()

        await session.close()


asyncio.run(insert_data())
