from pydantic_settings import BaseSettings, SettingsConfigDict

class _Settings(BaseSettings):
    ACCESS_KEY: str
    SECRET_KEY: str
    BUCKET_NAME: str
    ENDPOINT_URL: str
    DOMAIN: str

    #model_config = SettingsConfigDict(env_file="backend/app/settings/.env")
    model_config = SettingsConfigDict(env_file="C:/Users/Matvey/PycharmProjects/FileCloud/backend/app/settings/.env")

settings = _Settings()