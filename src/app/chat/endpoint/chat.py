from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, Depends
from fastapi.templating import Jinja2Templates
from dependency_injector.wiring import inject, Provide
from infrastructure.db.mongo import MongoDB
from app.chat.util.websocket_manager import ConnectionManager
from infrastructure.db.schema.chat import ChatModel
from app.chat.util.snow_flake import SnowflakeIdGenerator

router = APIRouter()
manager = ConnectionManager()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def root(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@router.websocket("/ws/{client_id}")
@inject
async def chat(websocket: WebSocket, client_id: int, mongodb: MongoDB = Depends(Provide["mongo"])):
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
