from fastapi import FastAPI
from minio import Minio
from starlette.middleware.cors import CORSMiddleware

from jobs_api.api.applicants.views import router as applicants_router
from jobs_api.api.employers.views import router as employers_router
from jobs_api.api.users.views import router as users_router
from jobs_api.api.vacancies.views import router as vacancies_router
from jobs_api.common.dependencies.s3 import get_minio_client
from jobs_api.settings import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(applicants_router, prefix="/api")
app.include_router(employers_router, prefix="/api")
app.include_router(vacancies_router, prefix="/api")
app.include_router(users_router, prefix="/api")


@app.on_event("startup")
def startup_event():
    minio_client = Minio(
        settings.MINIO_HOST,
        secret_key=settings.MINIO_SECRET_KEY,
        access_key=settings.MINIO_ACCESS_KEY,
        secure=False,
    )
    if not minio_client.bucket_exists(settings.MINIO_BUCKET):
        minio_client.make_bucket(settings.MINIO_BUCKET)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("jobs_api:app", host="localhost", port=8000, reload=True)
