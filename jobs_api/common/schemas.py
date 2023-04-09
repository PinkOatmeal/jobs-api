from pydantic import BaseModel


class BaseResponseSchema(BaseModel):
    class Config:
        orm_mode = True
