import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = os.getenv("APP_NAME")
    app_description: str = os.getenv("APP_DESCRIPTION")
    app_version: str = os.getenv("APP_VERSION")
    database_url: str = os.getenv("DATABASE_URL")
    secret_key: str = os.getenv("SECRET_KEY")
    algorithm: str = os.getenv("ALGORITHM")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"