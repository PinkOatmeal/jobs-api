from pydantic import BaseModel, EmailStr, Field


class EmployerSignUpForm(BaseModel):
    email: EmailStr
    password: str
    name: str


class EmployerReviewForm(BaseModel):
    text: str
    rating: int = Field(..., ge=1, le=5)
