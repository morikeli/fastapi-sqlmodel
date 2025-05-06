from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.review_schema import ReviewCreate
from app.services.review_service import ReviewService


router = APIRouter()
review_service = ReviewService()

@router.post('/book/{book_id}/add-review')
async def add_review_to_a_book(
    book_id: str,
    review_data: ReviewCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    new_review = await review_service.add_review_to_book(
        user_email=current_user.email,
        book_id=book_id,
        review_data=review_data,
        session=session,
    )

    return new_review
