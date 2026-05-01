from typing import Annotated

from fastapi import Depends, Query, Request
from pydantic import BaseModel

from src.database import async_session_maker
from src.exceptions import NotAuthenticatedHTTPException, NotEnoughPermissionsHTTPException
from src.models.users import UserRole, UsersORM
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1, lt=100)]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get('access_token', None)
    if not token:
        raise NotAuthenticatedHTTPException
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_jwt(token)
    return data['user_id']


UserIdDep = Annotated[int, Depends(get_current_user_id)]


def get_db_manager():
    return DBManager(session_factory=async_session_maker)


async def get_db():
    async with get_db_manager() as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]


async def get_current_user(
    user_id: int = Depends(get_current_user_id), db: DBManager = Depends(get_db)
):
    return await db.users.get_one(id=user_id)


UserDep = Annotated[UsersORM, Depends(get_current_user)]


def require_role(*roles: UserRole):
    async def checker(user: UserDep):
        user_role = user.role if isinstance(user.role, UserRole) else UserRole(user.role)
        if user_role not in roles:
            raise NotEnoughPermissionsHTTPException
        return True

    return checker


RequireAdminDep = Depends(require_role(UserRole.ADMIN))
RequireOwnerDep = require_role(UserRole.HOTEL_OWNER)
RequireOwnerOrAdminDep = require_role(UserRole.HOTEL_OWNER, UserRole.ADMIN)
