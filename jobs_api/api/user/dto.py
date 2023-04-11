from jobs_api.common.dto import BaseDTO
from jobs_api.common.enums import Role


class UserDTO(BaseDTO):
    id: int
    role: Role
    email: str
