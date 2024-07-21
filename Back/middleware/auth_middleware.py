import requests
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

AUTH_SERVER_URL = "http://localhost:4000"

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method != "OPTIONS":
            headers = {key: value for key, value in request.headers.items()}
            response = requests.get(f"{AUTH_SERVER_URL}/api/auth/validateSession", headers=headers)

            if response.status_code != 200:
                raise HTTPException(status_code=403, detail="Authentication failed")

        return await call_next(request)
