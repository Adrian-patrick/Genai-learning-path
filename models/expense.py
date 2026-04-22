from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SAEnum, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base


class ExpenseCategory(str, Enum):
    FOOD = "Food"
    TRANSPORT = "Transport"
    SHOPPING = "Shopping"
    UTILITIES = "Utilities"
    ENTERTAINMENT = "Entertainment"
    HEALTH = "Health"
    RENT = "Rent"
    OTHER = "Other"


class ExpenseFilterCategory(str, Enum):
    ALL = "All"
    FOOD = "Food"
    TRANSPORT = "Transport"
    SHOPPING = "Shopping"
    UTILITIES = "Utilities"
    ENTERTAINMENT = "Entertainment"
    HEALTH = "Health"
    RENT = "Rent"
    OTHER = "Other"


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    category: Mapped[ExpenseCategory] = mapped_column(
        SAEnum(ExpenseCategory, native_enum=False, create_constraint=True, length=32),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
