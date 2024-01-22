from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return "Hello World!"


class LoginRequestDto(BaseModel):
    email: str
    password: str

class LoginResponseDto(BaseModel):
    success: bool

@app.post('/login')
def login(login_body:LoginRequestDto):
    
    if login_body.email == 'raspberry-pi@dgist.ac.kr' and login_body.password == 'qwerty1234':
        return LoginResponseDto(success=True)
    else:
        return LoginResponseDto(success=False)