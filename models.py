from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Category(str, Enum):
    spam = "spam"
    important = "important"
    promotion = "promotion"
    general = "general"


class RequestModel(BaseModel):
    email_text: str


class ResponseModel(BaseModel):
    category: Category
    reason: str = Field(..., max_length=200)


class PredictionLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email_text: str
    category: str
    reason: str
    created_at: datetime


class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email_text: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(30), nullable=False)
    reason: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
