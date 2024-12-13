from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    OPENAI_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()


@lru_cache(maxsize=None)  # Explicitly set maxsize for Python 3.7
def get_settings():
    return settings


env_vars = get_settings()
