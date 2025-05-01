from app.models.user import User
from app.schemas.auth_schema import UserCreate
from app.utils.auth import hash_password
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select


class AuthService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        stmt = select(User).where(User.email == email)
        result = await session.exec(stmt)
        user = result.first()
        return user


    async def user_exists(self, email: str, session: AsyncSession) -> bool:
        user = await self.get_user_by_email(email, session)
        
        # if not user:
            # return False
        
        return True if user else False


    async def create_user(self, user_data: UserCreate, session: AsyncSession):
        user_info = user_data.model_dump()
        new_user = User(**user_info)
        new_user.password = hash_password(user_info["password"])
        new_user.user_role = 'user'
        
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user
