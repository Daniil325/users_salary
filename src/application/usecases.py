from dataclasses import asdict, dataclass

from src.domain.models import User
from src.infra.auth.jwt import PasswordManager
from src.infra.database.repo import SalaryScheduleRepo, UserRepo
from src.infra.protocols import RedisRepo
from src.infra.logging import logger


@dataclass
class BaseRedisCommand:
    redis: RedisRepo
    
    async def check_redis(self, item: str):
        if await self.redis.get(item):
            logger.info("Get info from redis storage")
            return (await self.redis.get(item)).decode()
        return None


@dataclass
class GetSalaryCommand(BaseRedisCommand):
    repo: SalaryScheduleRepo
    
    async def __call__(self, username: str, user_id: str):
        if result := await self.check_redis(username):
            if self.is_this_user(user_id, result["id"]):
                return result
            logger.info("Access denied")
            return "Доступ запрещен"
        logger.info("Get info from database")
        result = await self.repo.get_by_username(username)
        if self.is_this_user(user_id, result.id):
            logger.info("Set info to redis storage")
            await self.redis.set(username, str(asdict(result)) if result is not None else "")
            return result
        logger.info("Access denied")
        return "Доступ запрещен"
    
    @staticmethod
    def is_this_user(user_id: str, user_id_payload: str):
        if user_id == user_id_payload:
            return True
        return False
    
    
@dataclass
class LoginCommand:
    user_repo: UserRepo
    password_manager: PasswordManager
    
    async def __call__(self, username: str, password: str):
        if not (user := await self.user_repo.get_by_username(username)):
            return None
        if not self.password_manager.validate_password(
            password=password, 
            hashed_password=user.password
        ):
            return None
        
        return user
    
    
@dataclass
class RegisterUserDto:
    name: str
    surname: str
    password: str
    salary: int
    username: str
    role_id: str
    
    
@dataclass
class RegisterUserCommand:
    user_repo: UserRepo
    password_manager: PasswordManager
    
    async def __call__(self, dto: RegisterUserDto):
        if await self.user_repo.get_by_username(dto.username):
            return None
        
        password = self.password_manager.hash_password(dto.password)
        dto.password = password
        item = User.create(**asdict(dto))
        await self.user_repo.add(item)
        return item
        
        