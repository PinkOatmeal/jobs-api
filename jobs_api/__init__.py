from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from jobs_api.api.applicants.views import router as applicants_router
from jobs_api.api.users.views import router as users_router
from jobs_api.settings import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(applicants_router, prefix="/api")
app.include_router(users_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("jobs_api:app", host="localhost", port=8000, reload=True)
