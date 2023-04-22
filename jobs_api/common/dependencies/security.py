from datetime import datetime, timedelta

import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from starlette import status

from jobs_api.api.users.dto import UserDTO
from jobs_api.common.enums import Role
from jobs_api.controllers.user import UserController
from jobs_api.settings import settings

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/user/sign_in",
    scopes={
        "applicant": Role.applicant,
        "employer": Role.employer
    }
)

APPLICANTS = [Role.applicant]
EMPLOYERS = [Role.employer]
ALL = [Role.applicant, Role.employer]

INVALID_CREDENTIALS = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


def authenticate(
    auth_form: OAuth2PasswordRequestForm = Depends(),
    user_controller: UserController = Depends(),
) -> str:
    if len(auth_form.scopes) != 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Too many scopes",
        )
    user = user_controller.get_by_email(auth_form.username)
    if not user:
        raise INVALID_CREDENTIALS
    if not bcrypt.checkpw(auth_form.password.encode("utf-8"), user.password.encode("utf-8")):
        raise INVALID_CREDENTIALS
    if user.role not in auth_form.scopes:
        raise INVALID_CREDENTIALS
    jwt_payload = {"sub": str(user.id), "role": user.role, "exp": datetime.utcnow() + timedelta(days=30)}
    access_token = jwt.encode(jwt_payload, settings.SECRET_KEY, settings.ALGORITHM)
    return access_token


def _get_current_user(token: str = Depends(oauth2_scheme), user_controller: UserController = Depends()) -> UserDTO:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if user_id := payload.get("sub"):
            if user := user_controller.get(user_id):
                return UserDTO.from_orm(user)
        raise INVALID_CREDENTIALS
    except JWTError as e:
        raise INVALID_CREDENTIALS


class Authorize:
    def __init__(self, roles: list[Role]):
        self.authorized_roles = roles

    def __call__(self, user: UserDTO = Depends(_get_current_user)) -> UserDTO:
        if user.role not in self.authorized_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights to use this method")
        return user
