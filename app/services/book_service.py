from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.books import Book
from app.schemas.book_schemas import BookCreateSchema, UpdateBookSchema


class BookService:
    async def get_all_books(self, session: AsyncSession):
        stmt = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(stmt)
        return result.all()
    

    async def get_current_user_books(self, user_id: str, session: AsyncSession):
        stmt = select(Book).filter_by(user_id=user_id).order_by(desc(Book.created_at))
        result = await session.exec(stmt)
        return result.all()
    

    async def get_a_book_by_id(self, book_id: str, session: AsyncSession):
        stmt = select(Book).where(Book.id == book_id)
        result = await session.exec(stmt)
        book = result.first()

        return book if book is not None else None
    

    async def create_a_book(self, book_data: BookCreateSchema, user_id:str, session: AsyncSession):
        req_data = book_data.model_dump()   # request data

        # Parse published_date correctly before creating the object
        new_book = Book(**req_data)
        new_book.user_id = user_id

        session.add(new_book)   # add the book to the session
        await session.commit()  # save the created book
        await session.refresh(new_book)
        return new_book
    

    async def update_a_book(self, book_id: str, book_data: UpdateBookSchema, session: AsyncSession):
        req_data = await self.get_a_book_by_id(book_id, session)
        update_book = book_data.model_dump()
        
        if not update_book:
            return None
        
        for keys, values in update_book.items():
            setattr(req_data, keys, values)
        
        await session.commit()
        # await session.refresh(update_book)
        return update_book
    

    async def delete_a_book(self, book_id: str, session: AsyncSession):
        delete_book = await self.get_a_book_by_id(book_id, session)
        
        if not delete_book:
            return None
    
        await session.delete(delete_book)
        await session.commit()
        return {}

