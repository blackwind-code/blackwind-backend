from fastapi import APIRouter, Depends
from pydantic import BaseModel
from fastapi_router_controller import Controller

from schema.dto.auth_dto import LoginRequestDto, LoginResponseDto, RegisterRequestDto, RegisterResponseDto
from service.auth_service import AuthService
router = APIRouter(prefix='/auth')

controller = Controller(router, openapi_tag={
    'name': 'auth-controller'
})

@controller.use()
@controller.resource()
class AuthController():
    def __init__(self, service = Depends(AuthService)) -> None:
        self.service = service

    @controller.route.post(
        '/login',
        summary='Get Object from DB', 
        response_model=LoginResponseDto)
    async def login(self, body: LoginRequestDto):
        self.service.login(body.email, body.password)

    @controller.route.post('/register', summary='Register user', response_model=RegisterResponseDto)
    async def register(self, body: RegisterRequestDto):
        self.service.register(body.username, body.email, body.password, body.student_id)