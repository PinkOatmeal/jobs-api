from fastapi import APIRouter, Body, Depends, HTTPException, status

from jobs_api.api.employers.schemas import SignInResponse, SignUpResponse
from jobs_api.api.employers.forms import EmployerSignUpForm
from jobs_api.common.dependencies.security import authenticate
from jobs_api.controllers.employer import EmployerController

router = APIRouter(prefix="/employer", tags=["Employers"])


@router.post("/sign_up", response_model=SignUpResponse, status_code=status.HTTP_201_CREATED)
def sign_up(form: EmployerSignUpForm = Body(...), controller: EmployerController = Depends()):
    if controller.get_by_email(form.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")
    return controller.create(form)
