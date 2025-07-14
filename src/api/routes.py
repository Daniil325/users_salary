from typing import Annotated, Any

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import BaseModel

from src.api.deps import (
    get_jwt_service,
    get_login_command,
    get_register_user_command,
    get_salary_command,
)
from src.application.usecases import (
    GetSalaryCommand,
    LoginCommand,
    RegisterUserCommand,
    RegisterUserDto,
)
from src.infra.auth.jwt import JWTService

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login/",
)


class UserModel(BaseModel):
    id: str
    name: str
    surname: str
    salary: int
    username: str
    role_id: str


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


def get_token_payload(
    jwt_service: Annotated[JWTService, Depends(get_jwt_service)],
    token: str = Depends(oauth2_scheme),
) -> dict[str, Any]:
    try:
        payload = jwt_service.decode(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


class LoginModel(BaseModel):
    username: str
    password: str


async def validate_auth_user(
    login_cmd: Annotated[LoginCommand, Depends(get_login_command)],
    username: str = Form(),
    password: str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    user = await login_cmd(username, password)

    if not user:
        raise unauthed_exc
    return user


@router.post("/login/", response_model=TokenInfo)
async def login(
    jwt_service: Annotated[JWTService, Depends(get_jwt_service)],
    user: UserModel = Depends(validate_auth_user),
):
    payload = {"username": user.username, "id": user.id, "role_id": user.role_id}
    token = jwt_service.encode(payload)

    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )
    
    
class SalaryResponse(BaseModel):
    salary: int
    username: str
    salary_schedule: list


@router.get("/", response_model=SalaryResponse | str)
async def get_user_salary(
    username: str,
    cmd: Annotated[GetSalaryCommand, Depends(get_salary_command)],
    payload: dict = Depends(get_token_payload),
):
    result = await cmd(username, payload["id"])
    return result
