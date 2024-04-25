import uuid
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from infra.database import get_session
from model.discord.discord_user import DiscordUser
from schema.dto.discord_dto import UpsertDiscordUserResonseDto


class DiscordService:
    def __init__(self, db_session: Session = Depends(get_session)):
        self.db_session = db_session

    def upsert(self, discord_user_id: uuid.UUId):
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
    
    def verify():
        pass