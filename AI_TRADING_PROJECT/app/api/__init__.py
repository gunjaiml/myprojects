from fastapi import APIRouter
from app.api.trading import router as treadingrouter


app_router = APIRouter()

app_router.include_router(treadingrouter,prefix="/trades",tags=["Trade"])