from pydantic import BaseModel

class LoginRequestDto(BaseModel):
    email: str
    password: str

class LoginResponseDto(BaseModel):
    success: bool