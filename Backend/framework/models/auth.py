from beanie import Document
from fastapi_users_db_beanie.access_token import BeanieBaseAccessToken, BeanieAccessTokenDatabase


class AccessToken(BeanieBaseAccessToken, Document):
    pass


async def get_access_token_db():
    yield BeanieAccessTokenDatabase(AccessToken)
