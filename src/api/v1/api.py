from fastapi import APIRouter

from api.v1.endpoints import notificaiton

api_router = APIRouter()
api_router.include_router(notificaiton.router, tags=["Notifications"], prefix="/notification")
