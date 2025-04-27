from app.db.database import init_db
from app.routers.books import router as book_router
from contextlib import asynccontextmanager
from fastapi import FastAPI


version = 'v1'

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Server is starting ...')
    await init_db()
    yield 
    print('Server has shutdown!')

app = FastAPI(
    title='Bookly',
    description='A simple book management API',
    version=version,
    lifespan=lifespan,
)

# include router
app.include_router(book_router, prefix=f'/api/{version}', tags=['books'])
