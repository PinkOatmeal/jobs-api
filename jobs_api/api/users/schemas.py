from jobs_api.common.schemas import BaseResponseSchema


class TokenResponse(BaseResponseSchema):
    access_token: str
    token_type: str = "bearer"
