import os

import FastApi as FastApi
from beanie import init_beanie

from Backend.framework.authentication import auth_backend, fastapi_users, google_oauth_client
from Backend.framework.database import db
from Backend.framework.models.auth import AccessToken
from Backend.framework.models.user import User
from Backend.framework.schemas.users import UserCreate, UserRead, UserUpdate

app = FastApi()
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"]
)

if os.getenv("OAUTH_ENABLED"):
    if os.getenv("GOOGLE_OAUTH"):
        app.include_router(
            fastapi_users.get_oauth_router(google_oauth_client, auth_backend, os.getenv("SECRET")),
            prefix="/auth/oauth/google",
            tags=['auth']
        )
        app.include_router(
            fastapi_users.get_oauth_associate_router(google_oauth_client, UserRead, os.getenv("SECRET")),
            prefix="/auth/oauth/associate/google"
        )


@app.on_event("startup")
async def on_startup():
    await init_beanie(
        database=db,
        document_models=[
            AccessToken,
            User
        ],
    )
