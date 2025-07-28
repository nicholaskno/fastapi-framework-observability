from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.dependencies import get_db
from app.observability.controller.userController import userController
from app.observability.schemas.userSchema import (
    MessageResponse, 
    RegisterRequest,
    LoginRequest, 
    UserResponse
)
from app.utils.auth import get_current_user_dependency


router_register = APIRouter(prefix = "/observability/register", tags=["Observability - Register"])
router_login = APIRouter(prefix = "/observability/login", tags=["Observability - Login"])
router_user = APIRouter(prefix = "/observability/user", tags=["Observability - User"], dependencies = [Depends(get_current_user_dependency)])


@router_register.post("/", response_model=MessageResponse)
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    user = userController(db)
    return await user.register(request)


@router_login.post("/", response_model=MessageResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db), response: Response = None):
    user = userController(db)
    login = await user.login(request)

    # Define HTTPOnly cookie
    response.set_cookie(
        key="token",
        value=login["access_token"],
        httponly=True,
        secure=False,  #TO-DO: change to True in production, create settings for this
        samesite="Lax",
        max_age=99999999  #TO-DO: change to 1 day in production, create settings for this
    )

    #TO-DO: Logger
    return {"message": "Login successful"}


@router_user.get("/", response_model=UserResponse)
async def get_user_data(request: Request):
    #TO-DO: Logger
    user_data = {
        'user': {
            "id": str(request.state.user.id),
            "name": request.state.user.name,
            "username": request.state.user.username,
            "email": request.state.user.email
        }
    }

    return user_data
