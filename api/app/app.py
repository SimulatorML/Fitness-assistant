from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from src.dependencies.redis import startup, shutdown 
from src.views import users, llm, redis


__all__ = ["get_application"]


def get_application() -> FastAPI:
    app = FastAPI(title="Fitness Assistant API")

    # Register startup and shutdown events for Redis
    app.add_event_handler("startup", startup)
    app.add_event_handler("shutdown", shutdown)

    # Add a root route for health check
    @app.get("/")
    async def root():
        return {"message": "Welcome to the Fitness Assistant API"}
    
    # request processors
    app.add_middleware(middleware_class=ProxyHeadersMiddleware, trusted_hosts=["*"])
    app.add_middleware(middleware_class=GZipMiddleware)
    app.add_middleware(middleware_class=TrustedHostMiddleware, allowed_hosts=("*",))
    app.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=("*",),
        allow_methods=("*",),
        allow_headers=("*",),
        allow_credentials=True,
    )

    # Adding api routers
    app.include_router(users.router, prefix="/api/v1")
    app.include_router(llm.router, prefix="/api/v1")
    app.include_router(redis.router, prefix="/api/v1/redis")  # Add Redis test route

    return app
