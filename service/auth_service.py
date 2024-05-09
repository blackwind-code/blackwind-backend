from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from infra.crypto import get_password_hash

from infra.database import get_session
from infra.verify import generate_verify_email_html, generate_verify_email_message
from model.auth.user import User
from schema.dto.auth_dto import LoginResponseDto, RegisterResponseDto, VerifyResponseDto
from service.mail_service import MailService


class AuthService:
    #메일 서비스와 db 시동걸기
    def __init__(self, db_session: Session = Depends(get_session), mail_service: MailService = Depends(MailService)) -> None:
        self.db_session = db_session
        self.mail_service = mail_service
    
    #회원가입에 대한 함수
    async def register(self, username: str, email: str, password: str, student_id: int, department: str):
        
        statement = select(User).where(User.email == email or User.student_id == student_id)
        user = self.db_session.exec(statement).one_or_none()


        #회원 가입을 할 때, (이메일 인증이 안되어 있나 or 이메일이 이미 등록되어 있나 or 아이다가 이미 등록되어 있나를 평가)
        if user is not None:
            if user.verified:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'The email verification of {user.email} has not been completed.')
            
            if user.email == email:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'The user of {user.email} already exists')
            if user.student_id == student_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'The user of {user.student_id} already exists')
        
        #위의 조건을 통과하면 = 새 계정이라면 패스워드를 해쉬해서, db에 등록한다.

        hash_and_salt = get_password_hash(password)

        # check the department
        new_user = User(
            username=username,
            email=email,
            password=hash_and_salt,
            student_id=student_id,
            department=department
        )

        self.db_session.add(new_user)
        self.db_session.commit()
        self.db_session.refresh(new_user)

        # 메세지에 실을 내용을 정의하고
        message = generate_verify_email_message(new_user.username, new_user.email, new_user.verify_token)
        # 메세지를 보낸다
        await self.mail_service.send_mail(new_user.email, message.as_string())

        return RegisterResponseDto(**new_user.model_dump())
    
    #로그인에 관한 함수
    async def login(self, email:str, password:str):
        if not user.verified:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'The email verification of {user.email} has not been completed.')
        hash_and_salt = get_password_hash(password)

        statement = select(User).where(User.email == email and User.password == hash_and_salt)
        user = self.db_session.exec(statement).one_or_none()

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found or invalid credentials')

        if not user.verified:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'The email verification of {user.email} has not been completed.')
        
        return LoginResponseDto(**user.model_dump())

    async def verify(self, token):
        
        statement = select(User).where(User.verify_token == token)
        user = self.db_session.exec(statement).one_or_none()

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The token is invalid.')

        if user.verified:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='The user was already verified.')

        user.verified = True

        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)

        return VerifyResponseDto(verified=user.verified)

    