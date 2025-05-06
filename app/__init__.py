from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from app.errors import (
    create_exception_handler,
    AccessTokenRequiredException,
    AccountNotVerifiedException,
    BookNotFoundException,
    InvalidTokenException,
    InvalidUserCredentialsException,
    PermissionRequiredException,
    RefreshTokenRequiredException,
    RevokedTokenException,
    UserAlreadyExistsException,
    UserNotFoundException
)
from app.middleware.auth import CustomAuthMiddleWare
from app.middleware.logging import CustomLoggingMiddleware
from app.routers.auth import router as auth_router
from app.routers.books import router as book_router
from app.routers.review import router as review_router


version = 'v1'

app = FastAPI(
    title='Bookly',
    description='A simple book management API',
    version=version,
)


# add middlewares
# app.add_middleware(
#     CORSMiddleware(
#         app=app,
#         allow_origins=["http://localhost:3000"],
#         allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
#         allow_headers=["*"],
#         allow_credentials=True,
#     ),
# )
# app.add_middleware(TrustedHostMiddleware(app, allowed_hosts=['localhost', '127.0.0.1'],))
app.add_middleware(CustomAuthMiddleWare)
app.add_middleware(CustomLoggingMiddleware)


# register custom exceptions
app.add_exception_handler(AccessTokenRequiredException, create_exception_handler(403, "Authentication required!"))
app.add_exception_handler(AccountNotVerifiedException, create_exception_handler(403, "Please check your email and verify your account to use the app."))
app.add_exception_handler(BookNotFoundException, create_exception_handler(404, "Book not found!"))
app.add_exception_handler(InvalidTokenException, create_exception_handler(401, "Invalid to expired token provided!"))
app.add_exception_handler(InvalidUserCredentialsException, create_exception_handler(400, "Invalid user credentials."))
app.add_exception_handler(PermissionRequiredException, create_exception_handler(403, "You don't have permission to access this resource."))
app.add_exception_handler(RefreshTokenRequiredException, create_exception_handler(401, "Please provide a refresh token."))
app.add_exception_handler(RevokedTokenException,create_exception_handler(401, "This token was revoked! Please login again."))
app.add_exception_handler(UserAlreadyExistsException, create_exception_handler(409, "User with this email exists!"))
app.add_exception_handler(UserNotFoundException, create_exception_handler(404, "User not found."))


@app.exception_handler(500)
async def internal_server_error(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "message": "Oops! Something went wrong :(",
        }
    )

# include router
app.include_router(auth_router, prefix=f'/api/{version}/auth', tags=['Authentication'])
app.include_router(book_router, prefix=f'/api/{version}', tags=['Books'])
app.include_router(review_router, prefix=f'/api/{version}', tags=['Book Review'])
