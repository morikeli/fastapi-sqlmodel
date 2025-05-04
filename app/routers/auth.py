from datetime import datetime, timedelta
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from app import errors
from app.core.config import Config
from app.core.dependencies import AccessTokenBearer, get_current_user, RefreshTokenBearer, RoleChecker
from app.db.database import get_db
from app.db.redis import add_token_to_blacklist
from app.mails.send_mail import create_message, mail
from app.schemas.auth_schema import ConfirmResetPasswordModel, EmailModel, PasswordResetModel, UserCreate, UserLogin
from app.schemas.user_schema import UserModel, UserResponse
from app.services.auth_service import AuthService
from app.utils.auth import (
    create_access_token, 
    create_url_safe_token, 
    decode_access_token, 
    decode_url_safe_token, 
    hash_password,
    verify_password,

)


router = APIRouter()
auth_service = AuthService()
role_checker = RoleChecker(['admin', 'user'])

REFRESH_TOKEN_EXPIRY = True


@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreate, bg_task: BackgroundTasks, session: AsyncSession = Depends(get_db)):
    email = user_data.email

    user_exists = await auth_service.user_exists(email, session)
    
    if user_exists:
        raise errors.UserAlreadyExistsException()

    new_user = await auth_service.create_user(user_data, session)
    
    private_key = create_url_safe_token({"email": email})
    email_verification_link = f"http://{Config.DOMAIN}/api/v1/auth/verify/{private_key}"
    html_msg = f"""
    <h1>Verify your email</h1>
    <p>Please click this <a href="{email_verification_link}">link<a/> to verify your email.</p>
    """

    message = create_message(
        recipients=[email],
        subject="Verify your email",
        body=html_msg
    )
    bg_task.add_task(mail.send_message, message)
    return {"message": "Account created successfully! Check your email to verify your account."}


@router.get('/verify/{user_private_key}')
async def verify_email(user_private_key: str, session: AsyncSession = Depends(get_db)):
    user_data = decode_url_safe_token(user_private_key)
    user_email = user_data.get('email')

    if not user_email:
        return JSONResponse(
            content={
                "message": "Could not verify your email. An error ocurred!",
            },
            status_code=500,
        )
    
    user = await auth_service.get_user_by_email(user_email, session)
    if not user:
        raise errors.UserNotFoundException()

    await auth_service.update_user(user, {'is_verified': True}, session)
    return JSONResponse(
        content={
            "message": "User account verified successfully!"
        },
        status_code=200,
    )
    

@router.post('/send-mail')
async def send_mail(emails: EmailModel):
    email = emails.email_addresses
    html = "<h1>Welcome to the app!</h1>"

    message = create_message(recipients=email, subject="Welcome new user", body=html)
    await mail.send_message(message)

    return JSONResponse(content={"message": "Email sent successfully!"})


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


@router.get('/user/me', response_model=UserModel)
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

