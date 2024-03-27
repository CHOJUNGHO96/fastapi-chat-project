from datetime import datetime

from odmantic import Field, Index, Model
from odmantic.query import desc


class ChatModel(Model):
    message_id: int
    message_from: str
    message_to: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "indexes": lambda: [
            Index(ChatModel.message_id, unique=True, name="message_id_unique"),
            Index(ChatModel.message_from, desc(ChatModel.message_id), name="message_from_message_id"),
            Index(ChatModel.message_to, desc(ChatModel.message_id), name="message_to_message_id"),
        ]
    }
