from fastapi import APIRouter, Body, Depends, HTTPException, status

from jobs_api.api.employers.forms import EmployerReviewForm, EmployerSignUpForm
from jobs_api.api.employers.schemas import (
    EmployerResponse,
    EmployerReviewResponse,
    EmployerReviewsResponse,
    SignUpResponse,
)
from jobs_api.common.dependencies.security import ALL, APPLICANTS, Authorize
from jobs_api.controllers.employer import EmployerController
from jobs_api.controllers.review import ReviewController
from jobs_api.dto import UserDTO

router = APIRouter(prefix="/employers", tags=["Employers"])


@router.post("/sign_up", response_model=SignUpResponse, status_code=status.HTTP_201_CREATED)
def sign_up(form: EmployerSignUpForm = Body(...), controller: EmployerController = Depends()):
    if controller.get_by_email(form.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")
    return controller.create(form)


@router.get("/{employer_id}", response_model=EmployerResponse)
def get_employer(
    employer_id: int,
    employer_controller: EmployerController = Depends(),
    user: UserDTO = Depends(Authorize(ALL)),
):
    if not employer_controller.exists(employer_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employer with id {employer_id} not found")
    return employer_controller.get_with_rating(employer_id)


@router.post("/reviews/{employer_id}", response_model=EmployerReviewResponse)
def post_review(
    employer_id: int,
    form: EmployerReviewForm,
    review_controller: ReviewController = Depends(),
    employer_controller: EmployerController = Depends(),
    user: UserDTO = Depends(Authorize(APPLICANTS)),
):
    if not employer_controller.exists(employer_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Employer with id {employer_id} does not exist"
        )
    return review_controller.create(employer_id, form, user)


@router.get("/reviews/{employer_id}", response_model=EmployerReviewsResponse)
def get_employer_reviews(
    employer_id: int,
    review_controller: ReviewController = Depends(),
    user: UserDTO = Depends(Authorize(APPLICANTS)),
):
    reviews = review_controller.get_by_employer_id(employer_id)
    return EmployerReviewsResponse(reviews=reviews)
