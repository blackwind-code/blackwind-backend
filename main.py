from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from infra.database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

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
async def login(login_body:LoginRequestDto):
    if login_body.email == 'raspberry-pi@dgist.ac.kr' and login_body.password == 'qwerty1234':
        return LoginResponseDto(success=True)
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")