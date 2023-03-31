from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasicCredentials

from jobs_api.common.dependencies.security import auth

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("")
def get_jobs(credentials: HTTPBasicCredentials = Depends(auth)):
    return {"message": "Hello World!"}
