from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    title: str
    description: str

    habr_url: str

    model_config = SettingsConfigDict(env_file='.env', extra='allow')


@lru_cache
def get_settings():
    return Settings()
