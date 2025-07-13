from dataclasses import dataclass
from datetime import datetime

from src.domain.base import Entity


@dataclass
class Role(Entity):
    name: str
    
    
@dataclass
class SalarySchedule(Entity):
    user_id: str
    next_date: datetime
    
    
@dataclass
class User(Entity):
    name: str
    surname: str
    password: str
    salary: int
    username: str
    role_id: str
    
    @classmethod
    def create(cls, name: str,
    surname: str,
    password: str,
    salary: int,
    username: str,
    role_id: str):
        inst = cls(name, surname, password, salary, username, role_id)
        return inst