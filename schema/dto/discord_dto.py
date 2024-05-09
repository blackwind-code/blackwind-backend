import uuid
from pydantic import BaseModel

class UpsertDiscordUserRequestDto(BaseModel):
    discord_user_id: int
    pass

class UpsertDiscordUserResonseDto(BaseModel):
    verify_token: str

class SyncDiscordUserRequestDto(BaseModel):
    verify_token: str
    id: uuid.UUID

class SyncDiscordUserResponseDto(BaseModel):
    user_id: uuid.UUID
    discord_id: uuid.UUID