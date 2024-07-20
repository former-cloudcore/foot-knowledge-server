import requests
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)

        headers = {key: value for key, value in request.headers.items()}
        response = requests.get("http://localhost:4000/api/auth/validateSession", headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=403, detail="Authentication failed")

        return await call_next(request)
