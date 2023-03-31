import csv

import requests
from sqlalchemy.orm import Mapped

from jobs_api.common.database.base import BaseModel
from jobs_api.common.types import int_pk


class GeoModel(BaseModel):
    __tablename__ = "geo"

    id: Mapped[int_pk]
    name: Mapped[str]
    parent_id: Mapped[int | None]
