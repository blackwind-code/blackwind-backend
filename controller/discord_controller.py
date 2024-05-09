from fastapi import APIRouter, Depends
from fastapi_router_controller import Controller

from schema.dto.discord_dto import SyncDiscordUserRequestDto
from service.discord_service import DiscordService

router = APIRouter(prefix='/discord')

controller = Controller(router, openapi_tag={
    'name': 'discord-controller'
})

@controller.use()
@controller.resource()
class DiscordController():
    def __init__(self, discord_service = Depends(DiscordService)) -> None:
        self.discord_service = discord_service

    # required jwt token
    @controller.route.post(
        '/sync',
        summary='Sync the discord accout with bw account')
    async def sync(self, dto: SyncDiscordUserRequestDto):
        self.discord_service.sync(dto.id, dto.verify_token)