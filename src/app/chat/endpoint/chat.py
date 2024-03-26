from datetime import datetime

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates

from app.chat.util.snow_flake import SnowflakeIdGenerator
from app.chat.util.websocket_manager import ConnectionManager
from infrastructure.db.mongo import MongoDB
from infrastructure.db.schema.chat import ChatModel

router = APIRouter()
manager = ConnectionManager()
templates = Jinja2Templates(directory="templates")


@router.get("/")
@inject
async def root(request: Request, recive_client_id: str, mongodb: MongoDB = Depends(Provide["mongo"])):
    login_id = request.state.user["login_id"]
    chat_data = await mongodb.engine.find(
        ChatModel,
        ((ChatModel.message_from == login_id) & (ChatModel.message_to == recive_client_id))
        | ((ChatModel.message_from == recive_client_id) & (ChatModel.message_to == login_id)),
        sort=ChatModel.message_id.asc(),
    )
    return templates.TemplateResponse(
        "chat.html",
        {"request": request, "login_id": login_id, "recive_client_id": recive_client_id, "chat_data": chat_data},
    )


@router.websocket("/ws/{login_id}/{recive_client_id}")
@inject
async def chat(
    websocket: WebSocket, login_id: str, recive_client_id: str, mongodb: MongoDB = Depends(Provide["mongo"])
):
    await manager.connect(websocket)
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
            # await manager.send_personal_message(f"{login_id}: {data}", websocket)
            await manager.broadcast(f"{login_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{login_id} left the chat")
