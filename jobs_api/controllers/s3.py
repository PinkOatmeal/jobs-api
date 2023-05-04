from fastapi import Depends, UploadFile
from minio import Minio

from jobs_api.common.dependencies.s3 import get_minio_client
from jobs_api.settings import settings


class S3Controller:
    def __init__(self, minio_client: Minio = Depends(get_minio_client)):
        self._minio_client = minio_client

    def put(self, upload_file: UploadFile, user_id: int) -> str:
        extension = upload_file.filename[upload_file.filename.find(".") + 1:]
        filename = f"{user_id}-avatar.{extension}"
        self._minio_client.put_object(
            settings.MINIO_BUCKET,
            filename,
            upload_file.file,
            upload_file.size,
            upload_file.content_type,
        )
        return filename

    def get(self):
        pass
