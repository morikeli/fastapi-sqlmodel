from app.schemas.book_schemas import Book, BookCreateSchema, UpdateBookSchema
from app.db.database import get_db
from app.services.book_service import BookService
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import List


router = APIRouter()
service = BookService()


@router.get('/books', response_model=List[Book])
async def get_all_books(session: AsyncSession = Depends(get_db)):
    books = await service.get_all_books(session)
    return books


@router.post('/books/create', response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: BookCreateSchema, session: AsyncSession = Depends(get_db)) -> dict:
    new_book = await service.create_a_book(book_data, session)    
    return new_book


@router.get('/book/{book_id}', response_model=Book)
async def get_a_book(book_id: str, session: AsyncSession = Depends(get_db)) -> dict:
    book = await service.get_a_book_by_id(book_id, session)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book

@router.patch('/books/{book_id}/update')
async def update_a_book(book_id: str, book_data: UpdateBookSchema, session: AsyncSession = Depends(get_db)) -> dict:
    updated_book = await service.update_a_book(book_id, book_data, session) 
    
    if not updated_book:    
        # return 404 if the book is not found
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book


@router.delete('/book/{book_id}/delete', status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_book(book_id: str, session: AsyncSession = Depends(get_db)) -> None:
    deleted_book = await service.delete_a_book(book_id, session)

    if deleted_book:
        raise HTTPException(status_code=404, detail="Book not found")

    return None
