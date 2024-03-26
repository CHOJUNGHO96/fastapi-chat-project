from datetime import datetime

from odmantic import Model


class ChatModel(Model):
    message_id: int
    message_from: str
    message_to: str
    content: str
    created_at: datetime
