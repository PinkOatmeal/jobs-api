from typing import cast

from pydantic import BaseModel as BaseForm
from sqlalchemy import select

from jobs_api.api.employers.forms import EmployerReviewForm
from jobs_api.common.controllers import BaseController
from jobs_api.database import ReviewModel
from jobs_api.dto import UserDTO


class ReviewController(BaseController[ReviewModel]):
    model = ReviewModel

    def create(self, employer_id: int, form: EmployerReviewForm, user: UserDTO) -> ReviewModel:
        model = ReviewModel(
            text=form.text,
            rating=form.rating,
            reviewer_id=user.id,
            employer_id=employer_id,
        )
        self.session.add(model)
        self.session.flush()
        self.session.refresh(model)
        return model

    def update(self, _id: int, form: BaseForm):
        raise NotImplemented

    def get_by_employer_id(self, employer_id: int) -> list[ReviewModel]:
        stmt = select(self.model).where(self.model.employer_id == employer_id)
        return cast(list[ReviewModel], self.session.scalars(stmt).all())
