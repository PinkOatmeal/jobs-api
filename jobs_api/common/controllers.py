from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from fastapi import Depends
from pydantic import BaseModel as BaseForm
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from jobs_api.common.database.base import BaseModel
from jobs_api.common.dependencies.db import get_db

T = TypeVar("T", bound=BaseModel)


class BaseController(Generic[T], metaclass=ABCMeta):
    model: T = ...

    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    @abstractmethod
    def create(self, form: BaseForm) -> T:
        raise NotImplemented

    def get(self, _id: int) -> T:
        stmt = select(self.model).where(self.model.id == _id)
        return self.session.scalar(stmt)

    @abstractmethod
    def update(self, _id: int, form: BaseForm):
        raise NotImplemented

    def delete(self, _id: int):
        stmt = delete(self.model).where(self.model.id == _id)
        self.session.execute(stmt)
