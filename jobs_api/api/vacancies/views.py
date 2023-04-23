from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import conlist
from starlette import status

from jobs_api.dto import UserDTO
from jobs_api.api.vacancies.forms import CreateVacancyForm
from jobs_api.api.vacancies.schemas import VacanciesResponse, VacancyResponse
from jobs_api.common.dependencies.security import ALL, APPLICANTS, Authorize, EMPLOYERS
from jobs_api.controllers.vacancy import VacancyController

router = APIRouter(prefix="/vacancies", tags=["Vacancies"])

QUERY_RANGE = Query(
    None, description="Optional. Pass two values to apply `between` operator with them", example=[34, 67]
)


@router.get("/{vacancy_id}", response_model=VacancyResponse)
def get_vacancy(
    vacancy_id: int,
    vacancy_controller: VacancyController = Depends(),
    user: UserDTO = Depends(Authorize(ALL)),
):
    if vacancy := vacancy_controller.get(vacancy_id):
        return vacancy
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get("", response_model=VacanciesResponse)
def get_vacancies(
    ids: list[int] | None = Query(None),
    geo: list[int] | None = Query(None),
    experience: conlist(int, min_items=2, max_items=2) | None = QUERY_RANGE,
    salary: conlist(int, min_items=2, max_items=2) | None = QUERY_RANGE,
    employers: list[int] | None = Query(None),
    limit: int = 100,
    offset: int = 0,
    vacancy_controller: VacancyController = Depends(),
    user: UserDTO = Depends(Authorize(ALL)),
):
    vacancies = vacancy_controller.get_many(limit, offset, ids, geo, experience, salary, employers)
    return VacanciesResponse(vacancies=vacancies)


@router.post("")
def create_vacancy(
    form: CreateVacancyForm,
    vacancy_controller: VacancyController = Depends(),
    user: UserDTO = Depends(Authorize(EMPLOYERS)),
):
    return vacancy_controller.create_as_employer(form, user)


@router.post("/favorites/{vacancy_id}", status_code=201)
def add_vacancy_to_favorites(
    vacancy_id: int,
    vacancy_controller: VacancyController = Depends(),
    user: UserDTO = Depends(Authorize(APPLICANTS)),
):
    if vacancy_controller.is_favorite(user.id, vacancy_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Vacancy is already in favorites")
    vacancy_controller.add_to_favorites(user.id, vacancy_id)


@router.get("/favorites/", response_model=VacanciesResponse)
def get_favorite_vacancies(
    vacancy_controller: VacancyController = Depends(),
    user: UserDTO = Depends(Authorize(APPLICANTS)),
):
    vacancies = vacancy_controller.get_favorite_vacancies(user.id)
    return VacanciesResponse(vacancies=vacancies)


@router.delete("/favorites/{vacancy_id}", status_code=204)
def remove_vacancy_from_favorites(
    vacancy_id: int,
    vacancy_controller: VacancyController = Depends(),
    user: UserDTO = Depends(Authorize(APPLICANTS)),
):
    if not vacancy_controller.is_favorite(user.id, vacancy_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Vacancy is not in favorites")
    vacancy_controller.remove_from_favorites(user.id, vacancy_id)
