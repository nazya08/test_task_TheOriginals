from fastapi import APIRouter
from src.presentation.api.auth import routers as auth_routers
from src.presentation.api.user import routers as user_routers
from src.presentation.api.board import routers as board_routers
from src.presentation.api.list import routers as list_routers
from src.presentation.api.card import routers as card_routers

api_router = APIRouter()

api_router.include_router(auth_routers.router, prefix="/auth", tags=["auth"])
api_router.include_router(user_routers.router, prefix="/users", tags=["user"])
api_router.include_router(board_routers.router, prefix="/boards", tags=["board"])
api_router.include_router(list_routers.router, prefix="/boards", tags=["list"])
api_router.include_router(card_routers.router, prefix="/boards", tags=["card"])


@api_router.get("/alive")
def alive():
    return {'status': 'ok'}
