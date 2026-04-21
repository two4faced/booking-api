from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.api.dependencies import get_db_manager
from src.exceptions import ObjectNotFoundException
from src.services.auth import AuthService


class AdminAuthService(AuthenticationBackend):
    async def login(self, request: Request) -> bool | RedirectResponse:
        form = await request.form()
        email, password = form['username'], form['password']

        try:
            async with get_db_manager() as db:
                user = await db.users.get_user_with_hashed_pass(email=email)
                if not AuthService(db).verify_password(password, user.hashed_password):
                    return False
        except ObjectNotFoundException:
            return False

        if user.role != 'admin':
            return False

        request.session['admin'] = str(user.id)

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request):
        return 'admin' in request.session
