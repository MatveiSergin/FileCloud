from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    PATH_LENGTH: int = 100