from fastapi import Depends, Request
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Any, List

from app.db.database import get_db
from app.db.redis import token_in_blacklist
from app.models.user import User
from app.services.auth_service import AuthService
from app.utils.auth import decode_access_token
from app import errors


auth_servide = AuthService()


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_access_token(token)

        if not self.token_valid(token):
            raise errors.InvalidTokenException()

        if await token_in_blacklist(token_data["jti"]):
            raise errors.RevokedTokenException()

        self.verify_access_token(token_data)
        return token_data

    def token_valid(self, token: str) -> bool:
        token_data = decode_access_token(token)

        if token_data is None:
            return False
        
        return True
    
    def verify_access_token(self, token_data):
        raise NotImplementedError("Subclasses must implement this method.")


class AccessTokenBearer(TokenBearer):
    def verify_access_token(self, token_data: dict):
        if token_data and token_data["refresh"]:
            raise errors.AccessTokenRequiredException()


class RefreshTokenBearer(TokenBearer):
    def verify_access_token(self, token_data: dict):
        if token_data and not token_data["refresh"]:
            raise errors.RefreshTokenRequiredException()


async def get_current_user(
    token: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_db),
):
    user_email = token["user"]["email"]
    user = await auth_servide.get_user_by_email(user_email, session)
    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles
    

    async def __call__(self, current_user: User = Depends(get_current_user)) -> Any:
        # Check if the user is verified
        if not current_user.is_verified:
            raise errors.AccountNotVerifiedException()
        
        if current_user.user_role in self.allowed_roles:
            return True

        raise errors.PermissionRequiredException()
