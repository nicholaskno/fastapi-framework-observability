from datetime import datetime, timedelta, timezone
from app.settings import settings
from jwt.exceptions import PyJWTError
from fastapi import  Request, Depends, HTTPException
from app.utils.dependencies import get_db
from app.observability.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import jwt
import uuid


# Dependency to get the current user from the JWT token
async def get_current_user_dependency(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    return await get_current_user(request, db)


# Create JWT token for user
async def create_jwt_token_observability(
    user_data,
    db: AsyncSession = None
):
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.auth_exp)
    jti = str(uuid.uuid4())

    payload = {
        'user': str(user_data.id),
        'exp': exp,
        'jti': jti
    }

    token = jwt.encode(payload, settings.auth_secret_key, settings.auth_algorithm)

    return {
        'access_token': token,
        'exp': exp.isoformat(),
        'user': {
            "id": str(user_data.id),
            "name": user_data.name,
            "username": user_data.username,
            "email": user_data.email
        }
    }


# Validate JWT token and get user data and JTI
async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    token = request.cookies.get("token")

    if not token:
        raise HTTPException(status_code=401, detail="Token not found")

    try:
        payload = jwt.decode(token, settings.auth_secret_key, algorithms=["HS256"])
        user_id = payload.get("user")
        jti = payload.get("jti")

        if not user_id or not jti:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Load user
        result = await db.execute(
            select(User).filter_by(id=user_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        request.state.jti = jti
        request.state.user = user

        return user

    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
