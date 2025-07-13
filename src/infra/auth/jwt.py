from datetime import datetime, timedelta
from typing import Any

import bcrypt
import jwt

from src.settings import AuthJWTSettings


class JWTService:

    def __init__(self, settings: AuthJWTSettings):
        self.settings = settings
        self.private_key = self.settings.private_key_path.read_text()
        self.public_key = self.settings.public_key_path.read_text()
        self.algorithm: str = self.settings.algorithm
        self.expire_minutes = self.settings.access_token_expire_minutes
        

    def encode(self, payload: dict[str, Any]):
        to_encode = payload.copy()
        now = datetime.utcnow()
        if self.settings.expire_timedelta:
            expire = now + self.settings.expire_timedelta
        else:
            expire = now + timedelta(minutes=self.expire_minutes)
        to_encode.update(
            exp=expire,
            iat=now,
        )
        encoded = jwt.encode(
            to_encode,
            self.private_key,
            algorithm=self.algorithm,
        )
        return encoded

    def decode(self, token: str | bytes) -> dict:
        decoded = jwt.decode(
            token,
            self.public_key,
            algorithms=[self.algorithm],
        )
        return decoded


class PasswordManager:

    @staticmethod
    def hash_password(
        password: str,
    ) -> bytes:
        salt = bcrypt.gensalt()
        pwd_bytes: bytes = password.encode()
        return bcrypt.hashpw(pwd_bytes, salt)

    @staticmethod
    def validate_password(
        password: str,
        hashed_password: bytes,
    ) -> bool:
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hashed_password,
        )