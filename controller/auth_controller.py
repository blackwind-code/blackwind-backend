from fastapi import APIRouter, Depends
from pydantic import BaseModel
from fastapi_router_controller import Controller

from schema.dto.auth_dto import LoginRequestDto, LoginResponseDto
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
        tags=['sample-controller'], 
        summary='Get Object from DB', 
        response_model=LoginResponseDto)
    async def login(self, body: LoginRequestDto):
        self.service.login(body.email, body.password)