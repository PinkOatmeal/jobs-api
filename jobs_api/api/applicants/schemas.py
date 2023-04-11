from jobs_api.common.enums import Role
from jobs_api.common.schemas import BaseResponseSchema


class SignUpResponse(BaseResponseSchema):
    id: int
    email: str


class SignInResponse(BaseResponseSchema):
    id: int
    role: Role = Role.applicant
