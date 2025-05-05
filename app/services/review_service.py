from fastapi import HTTPException, logger
from sqlmodel.ext.asyncio.session import AsyncSession

from app import errors
from app.models.books import Review
from app.schemas.review_schema import ReviewCreate
from app.services.auth_service import AuthService
from app.services.book_service import BookService


book_service = BookService()
auth_service = AuthService()


class ReviewService:
    async def add_review_to_book(self, user_email: str, book_id: str, review_data: ReviewCreate, session: AsyncSession):
        try:
            book = await book_service.get_a_book_by_id(book_id=book_id, session=session)
            user = await auth_service.get_user_by_email(email=user_email, session=session)

            # Check if user exists
            if not user:
                raise errors.UserNotFoundException()
            
            # Check if book exists
            if not book:
                raise errors.BookNotFoundException()
            
            # create review
            new_review = Review(**review_data.model_dump())
            new_review.user = user
            new_review.books = book

            session.add(new_review)
            await session.commit()
            await session.refresh(new_review)

            return new_review

        except Exception as e:
            await session.rollback()
            logger.logger.exception(e)
            raise HTTPException(status_code=500, detail="Oops! INTERNAL SERVER ERROR!")
