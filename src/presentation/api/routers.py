from fastapi import APIRouter
from src.presentation.api.auth import routers as auth_routers
from src.presentation.api.user import routers as user_routers

api_router = APIRouter()

api_router.include_router(auth_routers.router, prefix="/auth", tags=["auth"])
api_router.include_router(user_routers.router, prefix="/users", tags=["user"])


@api_router.get("/alive")
def alive():
    return {'status': 'ok'}
