from typing import cast

from pydantic import BaseModel as BaseForm
from sqlalchemy import select

from jobs_api.dto import UserDTO
from jobs_api.api.vacancies.forms import CreateVacancyForm
from jobs_api.common.controllers import BaseController
from jobs_api.database import VacancyModel


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
