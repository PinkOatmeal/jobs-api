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

    @property
    def SQLALCHEMY_DB_URI(self) -> str:
        return (
            f"postgresql+psycopg2://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}"
            f"/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = BASE_DIR / ".env"
        case_sensitive = True


settings = _Settings()

if __name__ == "__main__":
    print(settings.SQLALCHEMY_DB_URI)
