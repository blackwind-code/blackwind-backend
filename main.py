from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI 
from controller.auth_controller import AuthController

from infra.database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
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

app.include_router(AuthController.router(), tags=['Auth'])