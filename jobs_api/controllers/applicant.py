import bcrypt
from pydantic import BaseModel as BaseForm
from sqlalchemy import select

from jobs_api.api.applicants.forms import ApplicantSignUpForm
from jobs_api.common.controllers import BaseController
from jobs_api.database.applicant import ApplicantModel


class ApplicantController(BaseController[ApplicantModel]):
    model = ApplicantModel

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

    def get_by_email(self, email: str) -> ApplicantModel:
        stmt = select(self.model).where(self.model.email == email)
        return self.session.scalar(stmt)

    def update(self, _id: int, form: BaseForm):
        raise NotImplemented
