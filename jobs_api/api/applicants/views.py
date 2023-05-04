from fastapi import APIRouter, Body, Depends, HTTPException, UploadFile, status

from jobs_api.api.applicants.forms import ApplicantSignUpForm
from jobs_api.api.applicants.schemas import ApplicantResponse, SignUpResponse
from jobs_api.common.dependencies.security import ALL, APPLICANTS, Authorize
from jobs_api.controllers.applicant import ApplicantController
from jobs_api.controllers.s3 import S3Controller
from jobs_api.dto import UserDTO

router = APIRouter(prefix="/applicants", tags=["Applicants"])


@router.post("/sign_up", response_model=SignUpResponse, status_code=status.HTTP_201_CREATED)
def sign_up(form: ApplicantSignUpForm = Body(...), controller: ApplicantController = Depends()):
    if controller.get_by_email(form.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")
    return controller.create(form)


@router.post("/avatar", status_code=status.HTTP_201_CREATED, response_model=ApplicantResponse)
def upload_avatar(
    avatar: UploadFile,
    applicant_controller: ApplicantController = Depends(),
    s3_controller: S3Controller = Depends(),
    user: UserDTO = Depends(Authorize(APPLICANTS)),
):
    avatar_filename = s3_controller.put(avatar, user.id)
    return applicant_controller.set_avatar(user.id, avatar_filename)
