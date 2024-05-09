import uuid
from sqlmodel import SQLModel,Field
from model.auth.user import User

class Seminar(SQLModel, table=True):
    id : uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False)
    title : str
    speaker_id : uuid.UUID
    place : str
    schedule : int
    accept : bool = Field(default=False)
    listeners : str = Field(default='')