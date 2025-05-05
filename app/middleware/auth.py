from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class CustomAuthMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Allow unauthenticated access to specific routes
        allowed_paths = [
            "/api/v1/auth/login",
            "/api/v1/auth/signup",
            "/api/v1/auth/verify",
            "/api/v1/auth/reset-password",
            "api/v1/auth/confirm-reset-password",
        ]

        if any(request.url.path.startswith(path) for path in allowed_paths):
            return await call_next(request)
        

        if "Authorization" not in request.headers:
            return JSONResponse(
                content={
                    "message": "Not authenticated! Please login again to proceed.",
                },
                status_code=401
            )

        response = await call_next(request)
        return response 
