import pytest

from src.application.usecases import LoginCommand
from src.domain.models import SalarySchedule
from src.infra.auth.jwt import PasswordManager
from src.infra.database.mapping import UserInDb
from src.infra.database.repo import SalaryScheduleRepo, UserRepo


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_salary(mocker):
    repo = mocker.AsyncMock(spec=SalaryScheduleRepo)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_login_fail(mocker):
    user_repo = mocker.AsyncMock(spec=UserRepo)
    password_manager = mocker.AsyncMock(spec=PasswordManager)

    user_repo.get_by_username = mocker.AsyncMock(return_value=None)

    sut = LoginCommand(user_repo, password_manager)

    result = await sut("test_username", "test_password")

    assert result is None


@pytest.mark.unit
@pytest.mark.asyncio
async def test_login(mocker):
    user_repo = mocker.AsyncMock(spec=UserRepo)
    password_manager = mocker.AsyncMock(spec=PasswordManager)

    return_user = UserInDb(
        salary=525252,
        username="test",
        name="test",
        surname="test",
        password="test_password",
        role_id="474b7e60-03f7-4fe1-b0b0-b07977d2b64a",
        id="d8feca82-c014-48bb-a784-5f51569fe69f",
        salary_schedule=[
            SalarySchedule(
                id="d8feca82-c014-48bb-a784-5f51569fe69f",
                user_id="474b7e60-03f7-4fe1-b0b0-b07977d2b64a",
                next_date="2025-11-01T00:00:00",
            )
        ],
    )

    user_repo.get_by_username = mocker.AsyncMock(return_value=return_user)

    sut = LoginCommand(user_repo, password_manager)

    result = await sut("test_username", "test_password")

    assert result is not None
    assert result == return_user
