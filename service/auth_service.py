from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from infra.crypto import get_password_hash

from infra.database import get_session
from model.auth.user import User


class AuthService:
    def __init__(self, db_session: Session = Depends(get_session)) -> None:
        self.db_session = db_session

    async def register(self, username: str, email: str, password: str, student_id: int, department: str):
        
        # Get user with email
        statement = select(User).where(User.email == email)
        user = self.db_session.exec(statement).one_or_none()

        if user is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'The user of {user.email} already exists')
        
        if user.verified:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{user.email}')

        hash_and_salt = get_password_hash(password)
        User(
            username=username,
            email=email,
            password=hash_and_salt,
            student_id=student_id,
            department=department
        )
        pass
    async def login(self, email:str, password:str):
        pass

    async def verify(self):
        pass

    