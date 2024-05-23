from datetime import datetime

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates

from app.chat.domain.chat_model import ChatModel
from app.chat.services.friendship_service import Service as FriendShipService
from app.chat.util.snow_flake import SnowflakeIdGenerator
from app.chat.util.websocket_manager import ConnectionManager
from config import conf
from infrastructure.db.mongo import MongoDB

router = APIRouter()
manager = ConnectionManager()
config = conf()
templates = Jinja2Templates(directory=config.TEMPLATE_DIR)


@router.get("/")
@inject
async def root(
    request: Request,
    recive_client_id: str,
    mongodb: MongoDB = Depends(Provide["mongo"]),
    friend_ship_service: FriendShipService = Depends(Provide["chat.friend_ship_service"]),
):
    login_id = request.state.user["login_id"]
    friendship_ids: list[int] = await friend_ship_service.select(login_id=login_id, recive_client_id=recive_client_id)
    await mongodb.engine.configure_database([ChatModel])
    chat_data = await mongodb.engine.find(
        ChatModel,
        ((ChatModel.message_from == login_id) & (ChatModel.message_to == recive_client_id))
        | ((ChatModel.message_from == recive_client_id) & (ChatModel.message_to == login_id)),
        sort=ChatModel.message_id.asc(),
    )
    return templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            "login_id": login_id,
            "recive_client_id": recive_client_id,
            "chat_data": chat_data,
            "room_id": sum(friendship_ids),
        },
    )


@router.websocket("/ws/{login_id}/{recive_client_id}/{room_id}")
@inject
async def chat(
    websocket: WebSocket,
    login_id: str,
    recive_client_id: str,
    room_id: int,
    mongodb: MongoDB = Depends(Provide["mongo"]),
):
    await manager.connect(room_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await mongodb.engine.save(
                ChatModel(
                    message_id=SnowflakeIdGenerator(data_center_id=1, worker_id=1).next_id(),
                    message_from=login_id,
                    message_to=recive_client_id,
                    content=data,
                    created_at=datetime.utcnow(),
                )
            )
            await manager.broadcast(room_id, f"{login_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
        await manager.broadcast(room_id, f"Client #{login_id} left the chat")
