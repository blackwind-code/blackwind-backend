from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from fastapi_router_controller import Controller

from schema.dto.seminar_dto import CreateRequestDto, CreateResponseDto
from service.seminar_service import SeminarService
router = APIRouter(prefix='/seminar')

controller = Controller(router, openapi_tag={
    'name': 'Seminar-controller'
})

@controller.use()
@controller.resource()
class SeminarController():
    def __init__(self, service: SeminarService = Depends(SeminarService)) -> None:
        self.service = service

    @controller.route.post(
            '/create',
            summary='Create Seminar',
            response_model=CreateResponseDto)
    async def create(self, body: CreateRequestDto):
        return await self.service.create(body.title, body.speaker_id, body.place, body.schedule)
