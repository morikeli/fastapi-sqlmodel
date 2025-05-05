from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import time
import logging

logger = logging.getLogger('uvicorn.access')
# logger.disabled = True


class CustomLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # get response
        response = await call_next(request)
        processing_time = time.time() - start_time
        message = f"{request.method} - {request.url.path} - {response.status_code} completed after {processing_time}s"

        print(f'Message: {message}')
        return response
