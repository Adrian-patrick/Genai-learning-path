from repositories.expense_repository import ExpenseRepository
from schemas.expense_schema import ExpenseCreate, ExpenseUpdate
from models.expense import ExpenseCategory


class ExpenseService:
    def __init__(self, repository: ExpenseRepository):
        self.repository = repository

    def create_expense(self, payload: ExpenseCreate):
        return self.repository.create(
            title=payload.title.strip(),
            amount=payload.amount,
            category=payload.category,
        )

    def list_expenses(
        self,
        category: ExpenseCategory | None = None,
        skip: int = 0,
        limit: int = 10,
    ):
        return self.repository.list_all(category=category, skip=skip, limit=limit)

    def get_expense(self, expense_id: int):
        return self.repository.get_by_id(expense_id)

    def update_expense(self, expense_id: int, payload: ExpenseUpdate):
        expense = self.repository.get_by_id(expense_id)
        if expense is None:
            return None
        return self.repository.update(
            expense=expense,
            title=payload.title.strip(),
            amount=payload.amount,
            category=payload.category,
        )

    def delete_expense(self, expense_id: int) -> bool:
        expense = self.repository.get_by_id(expense_id)
        if expense is None:
            return False
        self.repository.delete(expense)
        return True

    def get_total_spending(self, category: ExpenseCategory | None = None) -> float:
        return self.repository.total_spending(category=category)
