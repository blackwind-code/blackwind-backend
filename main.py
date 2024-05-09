from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from fastapi_socketio import SocketManager
from controller.auth_controller import AuthController
from controller.internal.discord_internal_controller import DiscordInternalController

from controller.seminar_controller import SeminarController
from infra.database import create_db_and_tables
from controller.websocket.discord_endpoint import setup_discord_endpoint

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
socket_manager = SocketManager(app=app)

setup_discord_endpoint(socket_manager)

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
app.include_router(SeminarController.router(), tags=['Seminar'])
app.include_router(DiscordInternalController.router(), tags=['Discord Internal'])
