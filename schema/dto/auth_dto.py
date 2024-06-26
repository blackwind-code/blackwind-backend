#밖에 보이면 안되는 정보들과 그렇지 않은 것들을 분류
import uuid
from pydantic import BaseModel

class LoginRequestDto(BaseModel):
    email: str
    password: str

class LoginResponseDto(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    student_id: int
    department: str

class RegisterRequestDto(BaseModel):
    username: str
    email: str
    password: str
    student_id: int
    department: str

class RegisterResponseDto(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    student_id: int
    department: str

class VerifyRequestDto(BaseModel):
    token: str
class VerifyResponseDto(BaseModel):
    verified: bool