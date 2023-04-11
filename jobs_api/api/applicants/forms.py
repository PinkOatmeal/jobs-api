from pydantic import BaseModel, EmailStr, Field

from jobs_api.common.enums import Education, Role


class ApplicantSignUpForm(BaseModel):
    email: EmailStr
    password: str
    name: str
    surname: str
    experience: int = Field(..., description="Number of months of work experience")
    education: Education
    skills: list[str]
