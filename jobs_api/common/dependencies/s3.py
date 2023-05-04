from minio import Minio
from jobs_api.settings import settings


def get_minio_client() -> Minio:
    minio_client = Minio(
        settings.MINIO_HOST,
        secret_key=settings.MINIO_SECRET_KEY,
        access_key=settings.MINIO_ACCESS_KEY,
        secure=False,
    )
    yield minio_client
