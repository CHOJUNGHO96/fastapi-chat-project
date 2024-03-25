from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.user.services.friendship_service import Service as FriendShipService

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/friendship", response_class=HTMLResponse)
@inject
async def friendship(
    request: Request,
    friend_id: list[int] = Query(None),
    friend_ship_service: FriendShipService = Depends(Provide["user.friend_ship_service"]),
):
    friend_info = await friend_ship_service.get_select_friendship(
        friend_id=friend_id, user_id=request.state.user["user_id"]
    )
    return templates.TemplateResponse(name="friendship.html", context={"request": request, "friend_info": friend_info})
