from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from jobs_api.common.enums import Education, Role
from jobs_api.common.types import str_array
from jobs_api.database import UserModel


class ApplicantModel(UserModel):
    __tablename__ = "applicants"
    id: Mapped[int] = mapped_column(ForeignKey(f"{UserModel.__tablename__}.id"), primary_key=True)
    surname: Mapped[str]
    experience: Mapped[int]
    education: Mapped[Education] = mapped_column(Enum(Education, name="education"))
    skills: Mapped[str_array]

    favorite_vacancies = relationship("FavoriteVacancyModel")

    __mapper_args__ = {"polymorphic_identity": Role.applicant}
