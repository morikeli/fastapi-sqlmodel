from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import List

from app import errors
from app.core.dependencies import AccessTokenBearer, RoleChecker
from app.db.database import get_db
from app.schemas.book_schemas import Book, BookDetails, BookCreateSchema, UpdateBookSchema
from app.services.book_service import BookService


router = APIRouter()
service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(['admin', 'user']))


@router.get('/books', dependencies=[role_checker], response_model=List[Book])
async def get_all_books(
    session: AsyncSession = Depends(get_db), 
    token: dict = Depends(access_token_bearer)
):
    books = await service.get_all_books(session)
    return books


@router.get('/books/{user_id}', dependencies=[role_checker], response_model=List[Book])
async def get_books_created_by_a_user(
    user_id: str,
    session: AsyncSession = Depends(get_db), 
    token: dict = Depends(access_token_bearer)
):
    books = await service.get_current_user_books(user_id, session)
    return books


@router.post('/book/create', dependencies=[role_checker], response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_a_book(
    book_data: BookCreateSchema, 
    session: AsyncSession = Depends(get_db),
    token: dict = Depends(access_token_bearer)
) -> dict:
    
    user_id = token.get('user')["user_id"]
    new_book = await service.create_a_book(book_data, user_id, session)    
    return new_book


@router.get('/book/{book_id}', dependencies=[role_checker], response_model=BookDetails)
async def get_a_book(
    book_id: str, 
    session: AsyncSession = Depends(get_db),
    token: dict = Depends(access_token_bearer)
) -> dict:
    book = await service.get_a_book_by_id(book_id, session)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book

@router.patch('/books/{book_id}/update', dependencies=[role_checker],)
async def update_a_book(
    book_id: str, 
    book_data: UpdateBookSchema, 
    session: AsyncSession = Depends(get_db),
    token: dict = Depends(access_token_bearer)
) -> dict:
    updated_book = await service.update_a_book(book_id, book_data, session) 
    
    if not updated_book:    
        # return 404 if the book is not found
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book


@router.delete('/book/{book_id}/delete', dependencies=[role_checker], status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_book(
    book_id: str, 
    session: AsyncSession = Depends(get_db),
    token: dict = Depends(access_token_bearer)
) -> None:
    deleted_book = await service.delete_a_book(book_id, session)

    if deleted_book:
        raise HTTPException(status_code=404, detail="Book not found")

    return None
