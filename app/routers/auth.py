from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.dependencies import AccessTokenBearer, get_current_user, RefreshTokenBearer, RoleChecker
from app.db.database import get_db
from app.db.redis import add_token_to_blacklist
from app.schemas.auth_schema import UserCreate, UserLogin
from app.schemas.user_schema import UserResponse
from app.services.auth_service import AuthService
from app.utils.auth import create_access_token, decode_access_token, verify_password


router = APIRouter()
auth_service = AuthService()
role_checker = RoleChecker(['admin', 'user'])

REFRESH_TOKEN_EXPIRY = True


@router.post('/signup', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreate, session: AsyncSession = Depends(get_db)):
    email = user_data.email

    user_exists = await auth_service.user_exists(email, session)
    
    if user_exists:
        raise HTTPException(status_code=403, detail='User with email already exists!')

    new_user = await auth_service.create_user(user_data, session)
    return new_user


@router.post('/login')
async def login(user_credentials: UserLogin, session: AsyncSession = Depends(get_db)):
    email = user_credentials.email
    password = user_credentials.password

    user = await auth_service.get_user_by_email(email, session)

    if user is None:
        raise HTTPException(status_code=403, detail="Invalid user credentials!")
    

    password_valid = verify_password(password, user.password)

    if password_valid:
        access_token = create_access_token(
            data={
                "email": user.email,
                "user_id": user.id,
                "role": user.user_role,
            }
        )

        refresh_token = create_access_token(
            data={
                "email": user.email,
                "user_id": user.id,
            },
            expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
            refresh=True,
        )

        return JSONResponse(
            content={
                "message": "User logged in successfully!",
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        )


@router.get('/refresh-token')
async def refresh_token(
    token_data: dict = Depends(RefreshTokenBearer()),
):
    expiry_timestamp = token_data["exp"]
    
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(
            data={
                "email": token_data["user"]["email"],
                "user_id": token_data["user"]["user_id"],
            }
        )
        
        return JSONResponse(
            content={
                "message": "Access token refreshed successfully!",
                "access_token": new_access_token,
            }
        )    
    
    raise HTTPException(status_code=400, detail="Refresh token expired!")


@router.get('/user/me')
async def get_user_details(
    user = Depends(get_current_user),
    _: bool = Depends(role_checker),
):
    return user


@router.post('/logout', status_code=status.HTTP_200_OK)
async def logout(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details["jti"]
    await add_token_to_blacklist(jti)
    return JSONResponse(
        content={
            "message": "User logged out successfully!",
        }
    )

