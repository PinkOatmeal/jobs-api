from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status
import bcrypt

from jobs_api.api.user.dto import UserDTO
from jobs_api.controllers.user import UserController

_security = HTTPBasic()



def authenticate(
    credentials: HTTPBasicCredentials = Depends(_security),
    user_controller: UserController = Depends(),
) -> UserDTO:
    user = user_controller.get_by_email(credentials.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    if not bcrypt.checkpw(credentials.password.encode("utf-8"), user.password.encode("utf-8")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    return UserDTO.from_orm(user)

