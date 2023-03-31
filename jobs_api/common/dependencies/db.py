from sqlalchemy.orm import Session

from jobs_api.common.database import SessionLocal


def get_db() -> Session:
    db: Session
    with SessionLocal() as db:
        try:
            yield db
        finally:
            db.close()
