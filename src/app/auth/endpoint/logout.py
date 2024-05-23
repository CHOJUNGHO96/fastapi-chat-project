from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from config import conf

router = APIRouter()
config = conf()
templates = Jinja2Templates(directory=config.TEMPLATE_DIR)


@router.post("/logout")
async def logout():
    response = JSONResponse(content={"status": 200, "msg": "Suceess Logout."})
    response.delete_cookie(key="token_type")
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return response
