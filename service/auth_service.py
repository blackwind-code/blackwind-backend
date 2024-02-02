from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from infra.crypto import get_password_hash

from infra.database import get_session
from model.auth.user import User
from schema.dto.auth_dto import LoginResponseDto, RegisterResponseDto


class AuthService:
    def __init__(self, db_session: Session = Depends(get_session)) -> None:
        self.db_session = db_session

    async def register(self, username: str, email: str, password: str, student_id: int, department: str):
        
        statement = select(User).where(User.email == email or User.student_id == student_id)
        user = self.db_session.exec(statement).one_or_none()

        if user is not None:
            if user.email == email:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'The user of {user.email} already exists')
            if user.student_id == student_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'The user of {user.student_id} already exists')
            
        if user.verified:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'The email verification of {user.email} has not been completed.')

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

        return RegisterResponseDto(**new_user.model_dump())
    
    async def login(self, email:str, password:str):
        
        hash_and_salt = get_password_hash(password)

        statement = select(User).where(User.email == email and User.password == hash_and_salt)
        user = self.db_session.exec(statement).one_or_none()

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found or invalid credentials')

        return LoginResponseDto(**user.model_dump())

    async def verify(self):
        pass

    