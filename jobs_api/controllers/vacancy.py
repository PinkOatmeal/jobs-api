from typing import cast

from pydantic import BaseModel as BaseForm
from sqlalchemy import delete, insert, select

from jobs_api.api.vacancies.forms import CreateVacancyForm
from jobs_api.common.controllers import BaseController
from jobs_api.database import VacancyModel
from jobs_api.database.favorite__vacancy import FavoriteVacancyModel
from jobs_api.dto import UserDTO


class VacancyController(BaseController[VacancyModel]):
    model = VacancyModel

    def create(self, form: CreateVacancyForm) -> VacancyModel:
        raise NotImplemented("You need to use `create_as_employer` method!")

    def create_as_employer(self, form: CreateVacancyForm, user: UserDTO):
        model = VacancyModel(
            title=form.title,
            description=form.description,
            salary=form.salary,
            experience=form.experience,
            employer_id=user.id,
            geo_id=form.geo_id,
        )
        self.session.add(model)
        self.session.flush()
        self.session.refresh(model)
        return model

    def get_many(
        self,
        limit: int,
        offset: int,
        ids: list[int] | None = None,
        geo: list[int] | None = None,
        experience: tuple[int, int] | None = None,
        salary: tuple[int, int] | None = None,
        employers: list[int] | None = None,
    ) -> list[VacancyModel]:
        filters = []
        if ids:
            filters.append(self.model.id.in_(ids))
        if geo:
            filters.append(self.model.geo_id.in_(geo))
        if experience:
            filters.append(self.model.experience.between(*experience))
        if salary:
            filters.append(self.model.salary.between(*salary))
        if employers:
            filters.append(self.model.employer_id.in_(employers))
        stmt = select(self.model).where(*filters).limit(limit).offset(offset)
        return cast(list[VacancyModel], self.session.scalars(stmt).all())

    def update(self, _id: int, form: BaseForm):
        pass

    def add_to_favorites(self, user_id: int, vacancy_id: int) -> None:
        stmt = insert(FavoriteVacancyModel).values(user_id=user_id, vacancy_id=vacancy_id)
        self.session.execute(stmt)

    def remove_from_favorites(self, user_id: int, vacancy_id: int) -> None:
        stmt = delete(FavoriteVacancyModel).where(
            FavoriteVacancyModel.user_id == user_id, FavoriteVacancyModel.vacancy_id == vacancy_id
        )
        self.session.execute(stmt)

    def get_favorite_vacancies(self, user_id: int) -> list[VacancyModel]:
        stmt = (
            select(self.model)
            .join(FavoriteVacancyModel, FavoriteVacancyModel.vacancy_id == self.model.id)
            .where(FavoriteVacancyModel.user_id == user_id)
        )
        return cast(list[VacancyModel], self.session.scalars(stmt).all())

    def is_favorite(self, user_id: int, vacancy_id: int) -> bool:
        stmt = select(1).where(FavoriteVacancyModel.user_id == user_id, FavoriteVacancyModel.vacancy_id == vacancy_id)
        return self.session.scalar(stmt) is not None
