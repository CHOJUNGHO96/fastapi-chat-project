from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, text
from sqlalchemy.orm import mapped_column

from .base import Base


class Friendship(Base):
    __tablename__ = "friendship"
    __table_args__ = (CheckConstraint("user_id != friend_id", name="chk_user_friend"),)

    friendship_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey("user_info.user_id"), nullable=False)
    friend_id = mapped_column(Integer, ForeignKey("user_info.user_id"), nullable=False)
    reg_date = mapped_column(DateTime(True), server_default=text("now()"))
