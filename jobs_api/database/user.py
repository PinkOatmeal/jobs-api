from sqlalchemy.orm import Mapped, relationship

from jobs_api.common.database.base import BaseModel
from jobs_api.common.types import int_pk, role


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int_pk]
    name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    role: Mapped[role]

    __mapper_args__ = {"polymorphic_identity": "user", "polymorphic_on": "role"}
