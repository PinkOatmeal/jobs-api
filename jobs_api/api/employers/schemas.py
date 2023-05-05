from pydantic import validator

from jobs_api.common.enums import Role
from jobs_api.common.schemas import BaseResponseSchema


class SignUpResponse(BaseResponseSchema):
    id: int
    email: str


class SignInResponse(BaseResponseSchema):
    id: int
    role: Role = Role.employer


class EmployerReviewResponse(BaseResponseSchema):
    id: int
    text: str
    rating: int


class EmployerReviewsResponse(BaseResponseSchema):
    reviews: list[EmployerReviewResponse]


class EmployerResponse(BaseResponseSchema):
    id: int
    name: str
    email: str
    rating: float

    @validator("rating")
    def round_rating(cls, v: float) -> float:
        return round(v, 1)
