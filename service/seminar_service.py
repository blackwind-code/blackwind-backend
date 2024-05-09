import uuid
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from infra.database import get_session
from model.auth.user import User
from model.seminar import Seminar
from schema.dto.seminar_dto import CreateResponseDto


class SeminarService:
    #메일 서비스와 db 시동걸기
    def __init__(self, db_session: Session = Depends(get_session)): 
        self.db_session = db_session
    
    #세미나를 만드는 함수 (user이라는 건 상민선배가 미리 만들어 놓음 이걸 가져오는 식으로 하자, 프론트에서 timestamp로 변경된 값을 받아와 int 값으로 저장하자)
    async def create(self, title : str, speaker_id : uuid.UUID, place:str, schedule:int):

    #    스퍼커id로 유저를 찾아 -> 스피커에 그 유저를 대입을하고 나머지를 받아온 값으로 채운다
        # 유저처럼 세미나 객체를 만든다

        statement = select(User).where(User.id == speaker_id)
        user = self.db_session.exec(statement).one_or_none()

        if user is None :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The user of {speaker_id} don\'t exist')
        #회원 가입을 할 때, (이메일 인증이 안되어 있나 or 이메일이 이미 등록되어 있나 or 아이다가 이미 등록되어 있나를 평가)
        if not user.verified:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'The email verification of {user.email} has not been completed.')
            
        new_seminar = Seminar(
            title = title,
            speaker_id = speaker_id,
            place = place,
            schedule = schedule,
        )
        
        # check the department
  
        self.db_session.add(new_seminar)
        self.db_session.commit()
        self.db_session.refresh(new_seminar)

        
        return CreateResponseDto(**new_seminar.model_dump())
    
    