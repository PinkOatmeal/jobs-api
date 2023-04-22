from jobs_api.common.schemas import BaseResponseSchema


class VacancyResponse(BaseResponseSchema):
    id: int
    title: str
    description: str
    salary: int
    experience: int
    geo_id: int


class VacanciesResponse(BaseResponseSchema):
    vacancies: list[VacancyResponse]
