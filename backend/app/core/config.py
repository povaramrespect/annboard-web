from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core import MultiHostUrl
from datetime import timezone, timedelta

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str

    DEFAULT_PHONE_REGION: str = "RU"

    S3_ENDPOINT_URL: str
    S3_BUCKET_NAME: str
    S3_ACCESS_KEY: str
    S3_SECRET_ACCESS_KEY: str
    S3_REGION_NAME: str

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    TZ_OFFSET_HOURS: int = 3

    @property
    def TZ(self):
        return timezone(timedelta(hours=self.TZ_OFFSET_HOURS))

settings = Settings()