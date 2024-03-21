from odmantic import Model


class ChatModel(Model):
    message_id: int
    message_from: int
    message_to: int
    content: str
    created_at: str
