from pydantic import validator

from jobs_api.settings import settings
from jobs_api.common.enums import Education, Role
from jobs_api.common.schemas import BaseResponseSchema


class SignUpResponse(BaseResponseSchema):
    id: int
    email: str


class SignInResponse(BaseResponseSchema):
    id: int
    role: Role = Role.applicant


class ApplicantResponse(BaseResponseSchema):
    id: int
    name: str
    email: str
    surname: str
    experience: int
    education: Education
    skills: list[str]
    avatar: str

    @validator("avatar")
    def path_to_url(cls, v: str) -> str:
        return f"{settings.MEDIA_URL}/{settings.MINIO_BUCKET}/{v}"
