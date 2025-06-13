from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "S3 File Management"

    S3_BUCKET_NAME: str = ""
    ALLOWED_FILE_TYPES: list[str]


def get_settings() -> Settings:
    load_dotenv()
    return Settings()
