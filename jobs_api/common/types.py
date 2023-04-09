from typing import Annotated

from sqlalchemy import ARRAY, Enum, String
from sqlalchemy.orm import mapped_column

from jobs_api.common.enums import Role

int_pk = Annotated[int, mapped_column(primary_key=True)]

role = Annotated[Role, mapped_column(Enum(Role, name="role"))]

str_array = Annotated[list[str], mapped_column(ARRAY(String), server_default="{}")]
