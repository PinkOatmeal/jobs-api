from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from jobs_api.common.database.base import BaseModel
from jobs_api.common.types import int_pk


class ReviewModel(BaseModel):
    __tablename__ = "reviews"

    id: Mapped[int_pk]
    text: Mapped[str]
    rating: Mapped[int]

    reviewer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    employer_id: Mapped[int] = mapped_column(ForeignKey("employers.id"), index=True)
