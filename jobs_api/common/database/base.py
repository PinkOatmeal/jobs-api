from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from jobs_api import settings

engine = create_engine(settings.SQLALCHEMY_DB_URI)

SessionLocal = sessionmaker(bind=engine)


class BaseModel(DeclarativeBase):
    pass
