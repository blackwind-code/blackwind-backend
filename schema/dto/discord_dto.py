from pydantic import BaseModel

class UpsertDiscordUserRequestDto(BaseModel):
    discord_user_id: int
    pass

class UpsertDiscordUserResonseDto(BaseModel):
    verify_token: str