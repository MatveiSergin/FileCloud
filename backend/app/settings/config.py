from pydantic_settings import BaseSettings


class Config(BaseSettings):
    PATH_LENGTH: int = 100


config = Config()