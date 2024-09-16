import datetime
import uuid

from pydantic import BaseModel

class File(BaseModel):
    name: str
    lastmodified: datetime.datetime
    size: int
    type: str

class AuthRequest(BaseModel):
    success: bool
    user_id: uuid.UUID | None
    detail: str = None

class AuthResponse(BaseModel):
    detail: str


class ResponseSchema(BaseModel):
    success: bool
    detail: str | None = None