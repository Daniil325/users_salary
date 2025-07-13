from dataclasses import dataclass
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Uuid, LargeBinary
from sqlalchemy.orm import registry, relationship

from src.domain.models import User, Role, SalarySchedule

mapper_registry = registry()
metadata = mapper_registry.metadata


@dataclass
class UserInDb(User):
    salary_schedule: SalarySchedule


role_table = Table(
    "role",
    metadata,
    Column("id", Uuid(as_uuid=False, native_uuid=True), primary_key=True),
    Column("name", String, unique=True, nullable=False),
)

user_table = Table(
    "user",
    metadata,
    Column("id", Uuid(as_uuid=False, native_uuid=True), primary_key=True),
    Column("name", String, nullable=False),
    Column("surname", String, nullable=False),
    Column("password", LargeBinary, nullable=False),
    Column("salary", Integer, nullable=False),
    Column("username", String, unique=True, nullable=False),
    Column("role_id", Uuid(as_uuid=False, native_uuid=True), ForeignKey("role.id"), nullable=False),
)

salary_schedule_table = Table(
    "salary_schedule",
    metadata,
    Column("id", Uuid(as_uuid=False, native_uuid=True), primary_key=True),
    Column("user_id", Uuid(as_uuid=False, native_uuid=True), ForeignKey("user.id"), nullable=False),
    Column("next_date", DateTime, nullable=False),
)

mapper_registry.map_imperatively(
    UserInDb,
    user_table,
    properties={
        "salary_schedule": relationship(SalarySchedule, back_populates="user"),
        "role": relationship(Role, back_populates="user"),
        },
)

mapper_registry.map_imperatively(
    Role,
    role_table,
    properties={"user": relationship(UserInDb, back_populates="role")},
)

mapper_registry.map_imperatively(
    SalarySchedule,
    salary_schedule_table,
    properties={"user": relationship(UserInDb, back_populates="salary_schedule")},
)
