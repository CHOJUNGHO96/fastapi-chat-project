from typing import Annotated

from pydantic import EmailStr, Field

from model import BaseModel


class ModelTokenData(BaseModel):
    user_id: Annotated[int, Field(example="유저번호")]
    token_type: Annotated[str, Field(example="토큰타입")]
    access_token: Annotated[str, Field(example="토큰")]
    refresh_token: Annotated[str, Field(example="리프레시토큰")]


class ModelUserRegister(BaseModel):
    login_id: str = Field(example="로그인 아이디")
    password: str = Field(example="패스워드")
    email: EmailStr = Field(example="이메일")
    user_name: str = Field(example="이름")
