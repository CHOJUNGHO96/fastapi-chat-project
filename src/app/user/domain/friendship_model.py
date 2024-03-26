from pydantic import Field

from model import BaseModel


class ModelFriendShipRequestRegister(BaseModel):
    login_id: str = Field(example="로그인 아이디")
