import os
import uuid

from fastapi import Depends
from fastapi_users import FastAPIUsers, BaseUserManager, UUIDIDMixin
from fastapi_users.authentication import BearerTransport, AuthenticationBackend
from fastapi_users.authentication.strategy import AccessTokenDatabase, DatabaseStrategy
from httpx_oauth.clients.google import GoogleOAuth2

from Backend.framework.models.auth import AccessToken, get_access_token_db
from Backend.framework.models.user import User, get_user_db

bearer_transport = BearerTransport('auth/token')


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = os.getenv("RESET_PASSWORD_TOKEN_SECRET")
    verification_token_secret = os.getenv("VERIFICATION_TOKEN_SECRET")


async def get_database_strategy(
        access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db)) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, 3600)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


google_oauth_client = GoogleOAuth2(
    os.getenv("GOOGLE_OAUTH_CLIENT_ID", ""),
    os.getenv("GOOGLE_OAUTH_CLIENT_SECRET", "")
)

auth_backend = AuthenticationBackend(name="database", transport=bearer_transport, get_strategy=get_database_strategy())

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
