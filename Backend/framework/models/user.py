from typing import List

from beanie import Document
from fastapi_users_db_beanie import BeanieBaseUser, BeanieUserDatabase, BaseOAuthAccount
from pydantic import Field


class OAuthAccount(BaseOAuthAccount):
    pass


class User(BeanieBaseUser, Document):
    oauth_accounts: List[OAuthAccount] = Field(default_factory=list)


async def get_user_db():
    yield BeanieUserDatabase(User, OAuthAccount)
