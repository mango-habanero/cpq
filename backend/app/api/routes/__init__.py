from fastapi import APIRouter

from .quotes import router as quotes_router
from .servers import router as server_router

api_router = APIRouter()

api_router.include_router(
    server_router,
    prefix="/servers",
    tags=["servers"],
)

api_router.include_router(
    quotes_router,
    prefix="/quotes",
    tags=["quotes"],
)
