import uuid

from fastapi_users import schemas


class UserCreate(schemas.BaseUserCreate):
    pass


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass
