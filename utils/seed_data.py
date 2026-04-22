from sqlalchemy import func, select

from database.database import SessionLocal
from models.expense import Expense, ExpenseCategory


def seed_dummy_expenses() -> None:
    db = SessionLocal()
    try:
        existing_count = db.scalar(select(func.count()).select_from(Expense))
        if existing_count and existing_count > 0:
            return

        seed_items = [
            Expense(title="Pizza", amount=450.0, category=ExpenseCategory.FOOD),
            Expense(title="Bus Pass", amount=120.0, category=ExpenseCategory.TRANSPORT),
            Expense(title="Electricity Bill", amount=1800.0, category=ExpenseCategory.UTILITIES),
            Expense(title="Groceries", amount=2400.0, category=ExpenseCategory.FOOD),
            Expense(title="Movie Night", amount=600.0, category=ExpenseCategory.ENTERTAINMENT),
            Expense(title="Medicine", amount=350.0, category=ExpenseCategory.HEALTH),
            Expense(title="New Shoes", amount=2200.0, category=ExpenseCategory.SHOPPING),
            Expense(title="Rent", amount=12000.0, category=ExpenseCategory.RENT),
        ]

        db.add_all(seed_items)
        db.commit()
    finally:
        db.close()