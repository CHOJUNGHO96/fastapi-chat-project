from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/logout")
async def logout():
    response = JSONResponse(content={"status": 200, "msg": "Suceess Logout."})
    response.delete_cookie(key="token_type")
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return response
