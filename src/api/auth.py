from fastapi import APIRouter, HTTPException, Response, Request

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import (
    ObjectAlreadyExistsException,
    UserNotFoundException,
    UserNotFoundHTTPException,
    WrongPassOrEmailException,
    WrongPassOrEmailHTTPException,
    NotAuthenticatedHTTPException,
)
from src.schemas.users import UserRequestAdd, UserLogIn, User, UserPatch
from src.services.auth import AuthService

router = APIRouter(prefix='/auth', tags=['Авторизация и Аутентификация'])


@router.post('/register')
async def register_user(user_data: UserRequestAdd, db: DBDep):
    try:
        await AuthService(db).register_user(user_data)
    except ObjectAlreadyExistsException:
        raise HTTPException(status_code=409, detail='Данный пользователь уже зарегистрирован')

    return {'status': 'OK'}


@router.post('/login')
async def login_user(user_data: UserLogIn, response: Response, db: DBDep):
    try:
        access_token = await AuthService(db).login_user(user_data)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except WrongPassOrEmailException:
        raise WrongPassOrEmailHTTPException

    response.set_cookie('access_token', access_token)
    return {'access_token': access_token}


@router.get('/me')
async def get_me(user_id: UserIdDep, db: DBDep):
    user: User = await AuthService(db).get_me(user_id)  # type: ignore
    return user


@router.patch('/me')
async def change_me(user_id: UserIdDep, user_data: UserPatch, db: DBDep):
    await AuthService(db).change_me(user_id, user_data)
    return {'status': 'OK'}


@router.post('/logout')
async def logout(response: Response, request: Request):
    access_token = request.cookies.get('access_token')

    if not access_token:
        raise NotAuthenticatedHTTPException

    response.delete_cookie('access_token')
    return {'status': 'OK'}
