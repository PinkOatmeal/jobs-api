from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from jobs_api.common.database.base import BaseModel
from jobs_api.common.types import int_pk


class FavoriteVacancyModel(BaseModel):
    __tablename__ = "favorite__vacancy"

    user_id: Mapped[int_pk] = mapped_column(ForeignKey("applicants.id"), index=True)
    vacancy_id: Mapped[int_pk] = mapped_column(ForeignKey("vacancies.id"))
