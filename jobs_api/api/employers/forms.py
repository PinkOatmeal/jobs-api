from pydantic import BaseModel, EmailStr


class EmployerSignUpForm(BaseModel):
    email: EmailStr
    password: str
    name: str
