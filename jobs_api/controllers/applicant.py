import bcrypt
from fastapi import Depends
from pydantic import BaseModel as BaseForm
from sqlalchemy.orm import Session

from jobs_api.api.applicants.forms import ApplicantSignUpForm
from jobs_api.common.controllers import BaseController
from jobs_api.common.dependencies.db import get_db
from jobs_api.common.enums import Role
from jobs_api.controllers.user import UserController
from jobs_api.database import UserModel
from jobs_api.database.applicant import ApplicantModel


class ApplicantController(BaseController[ApplicantModel]):
    model = ApplicantModel

    def __init__(self, session: Session = Depends(get_db), user_controller: UserController = Depends()):
        super().__init__(session)
        self._user_controller = user_controller

    def create(self, form: ApplicantSignUpForm) -> ApplicantModel:
        model = self.model(
            name=form.name,
            email=form.email,
            password=bcrypt.hashpw(form.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
            role=Role.applicant,
            surname=form.surname,
            experience=form.experience,
            education=form.education,
            skills=form.skills,
        )
        self.session.add(model)
        self.session.flush()
        self.session.refresh(model)
        return model

    def get_by_email(self, email: str) -> UserModel:
        return self._user_controller.get_by_email(email)

    def update(self, _id: int, form: BaseForm):
        raise NotImplemented

    def set_avatar(self, _id: int, avatar: str) -> ApplicantModel:
        model = self.get(_id)
        model.avatar = avatar
        self.session.add(model)
        self.session.flush()
        self.session.refresh(model)
        return model
