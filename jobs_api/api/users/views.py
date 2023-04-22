from fastapi import APIRouter, Depends

from jobs_api.api.users.schemas import TokenResponse
from jobs_api.common.dependencies.security import authenticate

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/sign_in", response_model=TokenResponse)
def sign_in(access_token: str = Depends(authenticate)):
    return TokenResponse(access_token=access_token)
