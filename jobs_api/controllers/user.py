from pydantic import BaseModel as BaseForm
from sqlalchemy import select

from jobs_api.common.controllers import BaseController, T
from jobs_api.database import UserModel


class UserController(BaseController[UserModel]):
    model = UserModel

    def create(self, form: BaseForm) -> T:
        raise NotImplemented

    def get_by_email(self, email: str) -> UserModel:
        stmt = select(self.model).where(self.model.email == email)
        return self.session.scalar(stmt)

    def update(self, _id: int, form: BaseForm):
        raise NotImplemented
