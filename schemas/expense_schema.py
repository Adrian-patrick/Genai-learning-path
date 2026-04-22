from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from models.expense import ExpenseCategory


class ExpenseCreate(BaseModel):
    title: str = Field(
        min_length=1,
        description="Expense title.",
        examples=["Pizza"],
    )
    amount: float = Field(
        gt=0,
        description="Expense amount, must be greater than zero.",
        examples=[450.0],
    )
    category: ExpenseCategory = Field(
        description="Expense category chosen from the allowed enum values.",
        examples=[ExpenseCategory.FOOD],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Pizza",
                "amount": 450.0,
                "category": "Food",
            }
        }
    )


class ExpenseUpdate(BaseModel):
    title: str = Field(
        min_length=1,
        description="Updated expense title.",
        examples=["Pizza Night"],
    )
    amount: float = Field(
        gt=0,
        description="Updated expense amount, must be greater than zero.",
        examples=[500.0],
    )
    category: ExpenseCategory = Field(
        description="Updated expense category chosen from the allowed enum values.",
        examples=[ExpenseCategory.ENTERTAINMENT],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Pizza Night",
                "amount": 500.0,
                "category": "Entertainment",
            }
        }
    )


class ExpenseResponse(BaseModel):
    id: int = Field(description="Unique expense identifier.", examples=[1])
    title: str = Field(description="Expense title.", examples=["Pizza"])
    amount: float = Field(description="Expense amount.", examples=[450.0])
    category: ExpenseCategory = Field(description="Expense category.", examples=[ExpenseCategory.FOOD])
    created_at: datetime = Field(description="Creation timestamp.")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Pizza",
                "amount": 450.0,
                "category": "Food",
                "created_at": "2026-04-22T11:12:12.538478",
            }
        },
    )


class TotalSpendingResponse(BaseModel):
    total_spending: float = Field(
        description="Total spending across matching expenses.",
        examples=[12000.0],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_spending": 12000.0,
            }
        }
    )
