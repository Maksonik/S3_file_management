from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AmazonSettings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_prefix="AMAZON_", extra="ignore")

    ACCESS_KEY_ID: str = ""
    SECRET_ACCESS_KEY: str = ""
    BUCKET_NAME: str = ""


class Settings(BaseSettings):
    APP_NAME: str = "S3 File Management"

    AMAZON: AmazonSettings = Field(default_factory=AmazonSettings)

    S3_BUCKET_NAME: str = ""
    ALLOWED_FILE_TYPES: list[str]


def get_settings() -> Settings:
    load_dotenv()
    return Settings()
