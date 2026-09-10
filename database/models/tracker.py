from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from database.models import BaseModel

class Tracker(BaseModel):
    __tablename__ = "trackers"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    query: Mapped[str]
    chat_id: Mapped[int] = mapped_column(BigInteger)
    status: Mapped[bool] = mapped_column(default=True)
