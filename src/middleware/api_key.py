from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from src.core.config import settings


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Se for apenas GET, libera
        if request.method == "GET":
            return await call_next(request)

        # Se estiver em DEBUG, podemos liberar certas rotas
        if settings.DEBUG:
            if request.url.path.startswith("/docs") or request.url.path.startswith("/menu"):
                return await call_next(request)

        # Verifica o header com a chave
        api_key = request.headers.get("X-API-KEY")
        if api_key != settings.SECRET_KEY:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing API Key"
            )

        return await call_next(request)
