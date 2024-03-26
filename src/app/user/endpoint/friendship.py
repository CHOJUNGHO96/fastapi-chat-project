from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.user.domain.friendship_model import ModelFriendShipRequestRegister
from app.user.services.friendship_service import Service as FriendShipService

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/friendship", response_class=HTMLResponse)
@inject
async def friendship(
    request: Request,
    friend_id: str | None = None,
    friend_ship_service: FriendShipService = Depends(Provide["user.friend_ship_service"]),
):
    friend_info = await friend_ship_service.get_select_friendship(
        friend_id=friend_id, user_id=request.state.user["user_id"]
    )
    return templates.TemplateResponse(
        name="friendship.html",
        context={
            "request": request,
            "user_name": request.state.user["user_name"],
            "login_id": request.state.user["login_id"],
            "friend_info": friend_info,
        },
    )


@router.post("/friendship")
@inject
async def register_friendship(
    request: Request,
    friend_info: ModelFriendShipRequestRegister,
    friend_ship_service: FriendShipService = Depends(Provide["user.friend_ship_service"]),
):
    if await friend_ship_service.register_friendship(
        friend_id=friend_info.login_id, user_id=request.state.user["user_id"]
    ):
        return JSONResponse(content={"msg": "Success Registrate News List.", "code": "200"})
    else:
        return JSONResponse(status_code=422, content={"msg": "Fail to news registrate", "code": "422"})
