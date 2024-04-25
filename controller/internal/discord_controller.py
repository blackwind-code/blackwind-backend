from fastapi import APIRouter, Depends
from fastapi_router_controller import Controller

from schema.dto.discord_dto import UpsertDiscordUserRequestDto, UpsertDiscordUserResonseDto
from service.discord_service import DiscordService

router = APIRouter(prefix='/discord')

controller = Controller(router, openapi_tag={
    'name': 'discrod-controller'
})

@controller.use()
@controller.resource()
class DiscordController():
    def __init__(self, service = Depends(DiscordService)) -> None:
        self.service = service

    @controller.route.put(
        '/user',
        summary='Emit the user in entering guild events', 
        response_model=UpsertDiscordUserResonseDto)
    async def upsert(self, body: UpsertDiscordUserRequestDto):
        return await self.service.upsert(body.discord_user_id)