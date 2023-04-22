from pydantic import BaseModel, Field


class CreateVacancyForm(BaseModel):
    title: str
    description: str
    salary: int
    experience: int = Field(..., description="Number of months of work experience")
    geo_id: int
