import uuid
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from infra.database import get_session
from model.auth.user import User
from model.discord.discord_user import DiscordUser
from schema.dto.discord_dto import SyncDiscordUserResponseDto, UpsertDiscordUserResonseDto


class DiscordService:
    def __init__(self, db_session: Session = Depends(get_session)):
        self.db_session = db_session

    async def upsert(self, discord_user_id: uuid.UUID):
        statement = select(DiscordUser).where(DiscordUser.discord_user_id == discord_user_id)
        discord_user = self.db_session.exec(statement).one_or_none()
        
        if discord_user:
            if discord_user.user is not None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'The discord account is connected to other user.')
            
            return UpsertDiscordUserResonseDto(verify_token= discord_user.verify_token)


        new_discord_user = DiscordUser(
            discord_user_id=discord_user_id
        )

        self.db_session.add(new_discord_user)
        self.db_session.commit()
        self.db_session.refresh(new_discord_user)

        return UpsertDiscordUserResonseDto(verify_token= new_discord_user.verify_token)
    
    async def sync(self, user_id: uuid.UUID, verify_token: str):

        statement = select(DiscordUser).where(DiscordUser.verify_token == verify_token)
        discord_user = self.db_session.exec(statement).one_or_none()

        if discord_user is None:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Discord Account Not Found ')
        
        statement = select(User).where(User.id == user_id)
        user = self.db_session.exec(statement).one_or_none()

        if user is None:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User Account Not Found ')

        discord_user.user = user
        self.db_session.add(discord_user)
        self.db_session.commit()
        self.db_session.refresh()

        return SyncDiscordUserResponseDto(
            user_id=user.id,
            discord_id=discord_user.id
        )

