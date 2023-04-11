from fastapi import APIRouter, Body, Depends, HTTPException, status

from jobs_api.api.applicants.forms import ApplicantSignUpForm
from jobs_api.api.applicants.schemas import SignInResponse, SignUpResponse
from jobs_api.common.dependencies.security import authenticate
from jobs_api.controllers.applicant import ApplicantController

router = APIRouter(prefix="/applicants", tags=["Applicants"])


@router.post("/sign_up", response_model=SignUpResponse)
def sign_up(form: ApplicantSignUpForm = Body(...), controller: ApplicantController = Depends()):
    if controller.get_by_email(form.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")
    return controller.create(form)


@router.post("/sign_in")
def sign_in(user_id: int = Depends(authenticate)):
    return SignInResponse(id=user_id)