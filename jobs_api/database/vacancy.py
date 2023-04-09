from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from jobs_api.common.database.base import BaseModel
from jobs_api.common.types import int_pk


class Vacancy(BaseModel):
    __tablename__ = "vacancies"

    id: Mapped[int_pk]
    title: Mapped[str]
    description: Mapped[str]
    salary: Mapped[int]
    experience: Mapped[int]

    employer_id: Mapped[int] = mapped_column(ForeignKey("employers.id", name="vacancy_author_fk"), index=True)
    employer = relationship("EmployerModel", back_populates="vacancies")

    geo_id: Mapped[int] = mapped_column(ForeignKey("geo.id", name="vacancy_geo_fk"), index=True)
    geo = relationship("GeoModel")
