import os
from pathlib import Path

from pydantic import BaseSettings

BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class _Settings(BaseSettings):
    PROJECT_NAME: str = "Jobs API"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    MINIO_HOST: str = "127.0.0.1:9000"
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET: str = "jobs"

    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    @property
    def SQLALCHEMY_DB_URI(self) -> str:
        return (
            f"postgresql+psycopg2://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}"
            f"/{self.POSTGRES_DB}"
        )

    @property
    def MEDIA_URL(self) -> str:
        return f"http://{self.MINIO_HOST}"

    class Config:
        env_file = BASE_DIR / ".env"
        case_sensitive = True


settings = _Settings()
