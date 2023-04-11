import bcrypt
from fastapi import Depends
from pydantic import BaseModel as BaseForm
from sqlalchemy.orm import Session

from jobs_api.api.employers.forms import EmployerSignUpForm
from jobs_api.common.controllers import BaseController
from jobs_api.common.dependencies.db import get_db
from jobs_api.common.enums import Role
from jobs_api.controllers.user import UserController
from jobs_api.database import EmployerModel, UserModel


class EmployerController(BaseController[EmployerModel]):
    model = EmployerModel

    def __init__(self, session: Session = Depends(get_db), user_controller: UserController = Depends()):
        super().__init__(session)
        self._user_controller = user_controller

    def create(self, form: EmployerSignUpForm) -> EmployerModel:
        model = self.model(
            name=form.name,
            email=form.email,
            password=bcrypt.hashpw(form.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
            role=Role.employer,
        )
        self.session.add(model)
        self.session.flush()
        self.session.refresh(model)
        return model

    def get_by_email(self, email: str) -> UserModel:
        return self._user_controller.get_by_email(email)

    def update(self, _id: int, form: BaseForm):
        pass
