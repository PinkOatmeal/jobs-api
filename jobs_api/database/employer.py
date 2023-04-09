from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from jobs_api.common.enums import Role
from jobs_api.database import UserModel


class EmployerModel(UserModel):
    __tablename__ = "employers"
    id: Mapped[int] = mapped_column(ForeignKey(f"{UserModel.__tablename__}.id"), primary_key=True)
    rating: Mapped[int | None]

    vacancies = relationship("Vacancy", back_populates="employer")

    __mapper_args__ = {
        "polymorphic_identity": Role.employer
    }
