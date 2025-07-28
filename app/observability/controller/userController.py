from fastapi import HTTPException
from app.observability.models.user import User
from app.base.baseController import baseController
from app.utils.auth import create_jwt_token_observability
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
import bcrypt
import logging

logger = logging.getLogger("observability")


class userController(baseController):
    def __init__(self, db, query_params = None) -> None:
        super().__init__(User, 'User', db, query_params)


    async def register(self, request):
        try:
            existing_user = await self.get_user(email=request.email, username=request.username)

            if existing_user:
                logger.warning(f"Warning - User with email {request.email} or username {request.username} already exists.")
                raise HTTPException(status_code=400, detail="Username or email already exists")

            user = User(
                name=request.name,
                email=request.email,
                username=request.username,
                hashed_password=self.hash_password(request.password),
                status="active"
            )

            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)

            logger.info(f"Info - User {user.username} registered successfully.")
            return {"message": "User registered successfully"}

        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail="Database error")
    

    async def login(self, request):
        user = await self.get_user(username=request.username)

        if not user or not self.verify_password(request.password, user.hashed_password):
            logger.warning(f"Warning - Login failed for user {request.username}. Invalid credentials.")
            raise HTTPException(status_code=400, detail="Invalid username or password")

        if user.status != "active":
            logger.warning(f"Warning - Login failed for user {user.username}. User is not active.")
            raise HTTPException(status_code=400, detail="User not active")


        logger.info(f"Info - User {user.username} logged in successfully.")
        return await create_jwt_token_observability(user, self.db)

     
    async def get_user(self, email: str = None, username: str = None):
        stmt = select(User)

        if email and username:
            stmt = stmt.where(
                (User.email == email) | (User.username == username)
            )
        elif email:
            stmt = stmt.where(User.email == email)
        elif username:
            stmt = stmt.where(User.username == username)

        result = await self.db.execute(stmt)
        user = result.scalars().first()
        return user


    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    