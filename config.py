from functools import lru_cache

import requests
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    S3_BUCKET_NAME: str
    COGNITO_REGION: str
    COGNITO_USER_POOL_ID: str
    COGNITO_CLIENT_ID: str
    COGNITO_CLIENT_SECRET: str
    JWKS: dict

    POSTGRES_DBNAME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    CELERY_BROKER: str

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def _get_settings():
    settings = Settings()

    response = requests.get(
        f"https://cognito-idp.{settings.COGNITO_REGION}.amazonaws.com/{settings.COGNITO_USER_POOL_ID}/.well-known/jwks.json"
    )
    if response.status_code != 200:
        raise RuntimeError("Could not retrieve JWKS")

    settings.JWKS = response.json()

    return settings


settings = _get_settings()
