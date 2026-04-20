from datetime import datetime, timezone

from pydantic import BaseModel,Field
from database import Base
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped ,mapped_column

class RequestModel(BaseModel):
    query: str = Field(..., example="Plan a trip to goa for 5 days")

class ResponseModel(BaseModel):
    answer: str

class Conversation(Base):
    __tablename__ = "conversations"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    query:Mapped[str] = mapped_column(String(255), nullable=False)
    # Changed: use Text because LLM outputs often exceed 255 chars and can fail inserts.
    answer:Mapped[str] = mapped_column(Text, nullable=False)
    # Changed: persist creation timestamp so history shows when each response was generated.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
