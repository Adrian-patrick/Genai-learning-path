from sqlalchemy import func, select
from sqlalchemy.orm import Session

from models.expense import Expense, ExpenseCategory


class ExpenseRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, title: str, amount: float, category: ExpenseCategory) -> Expense:
        expense = Expense(title=title, amount=amount, category=category)
        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def list_all(
        self,
        category: ExpenseCategory | None = None,
        skip: int = 0,
        limit: int = 10,
    ) -> list[Expense]:
        stmt = select(Expense)
        if category:
            stmt = stmt.where(Expense.category == category)
        stmt = stmt.offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, expense_id: int) -> Expense | None:
        stmt = select(Expense).where(Expense.id == expense_id)
        return self.db.scalars(stmt).first()

    def update(self, expense: Expense, title: str, amount: float, category: ExpenseCategory) -> Expense:
        expense.title = title
        expense.amount = amount
        expense.category = category
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def delete(self, expense: Expense) -> None:
        self.db.delete(expense)
        self.db.commit()

    def total_spending(self, category: ExpenseCategory | None = None) -> float:
        stmt = select(func.coalesce(func.sum(Expense.amount), 0.0))
        if category:
            stmt = stmt.where(Expense.category == category)
        total = self.db.execute(stmt).scalar_one()
        return float(total)
