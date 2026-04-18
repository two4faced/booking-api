from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Literal


class Settings(BaseSettings):
    MODE: Literal['TEST', 'LOCAL', 'DEV', 'PROD']

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    CACHE_HOST: str
    CACHE_PORT: int

    @property
    def CACHE_URL(self):
        return f'redis://{self.CACHE_HOST}:{self.CACHE_PORT}'

    @property
    def DB_URL(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def ADMIN_DB_URL(self):
        return f'postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()  # type: ignore
