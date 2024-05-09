import uuid
from pydantic import BaseModel
from model.auth.user import User

class  CreateRequestDto(BaseModel):
    title : str
    speaker_id : str
    place : str
    schedule : int

class  CreateResponseDto(BaseModel):
    id: uuid.UUID
    title : str
    speaker_id: uuid.UUID
    place : str
    schedule : int
    