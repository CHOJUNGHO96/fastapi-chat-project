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
async def root(request: Request):
    login_id = request.state.user["login_id"]
    return templates.TemplateResponse("chat.html", {"request": request, "login_id": login_id})


@router.websocket("/ws/{login_id}")
@inject
async def chat(websocket: WebSocket, client_id: str, mongodb: MongoDB = Depends(Provide["mongo"])):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await mongodb.engine.save(
                ChatModel(
                    message_id=SnowflakeIdGenerator(data_center_id=1, worker_id=1).next_id(),
                    message_from=client_id,
                    message_to=4186,
                    content=data,
                    created_at="2021-10-10 10:10:10",
                )
            )
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
