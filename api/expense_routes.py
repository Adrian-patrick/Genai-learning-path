from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from database.database import get_db
from models.expense import ExpenseCategory, ExpenseFilterCategory
from repositories.expense_repository import ExpenseRepository
from schemas.expense_schema import (
    ExpenseCreate,
    ExpenseResponse,
    ExpenseUpdate,
    TotalSpendingResponse,
)
from services.expense_service import ExpenseService


router = APIRouter(
    prefix="/expenses",
    tags=["expenses"],
)


def get_expense_service(db: Session = Depends(get_db)) -> ExpenseService:
    repository = ExpenseRepository(db)
    return ExpenseService(repository)


@router.post("", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    payload: ExpenseCreate,
    service: ExpenseService = Depends(get_expense_service),
):
    return service.create_expense(payload)


@router.get("", response_model=list[ExpenseResponse])
def get_expenses(
    category: ExpenseFilterCategory = Query(default=ExpenseFilterCategory.ALL),
    skip: int = Query(default=0, ge=0, description="Number of expenses to skip."),
    limit: int = Query(default=10, ge=1, le=100, description="Maximum number of expenses to return."),
    service: ExpenseService = Depends(get_expense_service),
):
    return service.list_expenses(category=None if category == ExpenseFilterCategory.ALL else ExpenseCategory(category.value), skip=skip, limit=limit)


@router.get("/total", response_model=TotalSpendingResponse)
def get_total_spending(
    category: ExpenseFilterCategory = Query(default=ExpenseFilterCategory.ALL),
    service: ExpenseService = Depends(get_expense_service),
):
    total = service.get_total_spending(category=None if category == ExpenseFilterCategory.ALL else ExpenseCategory(category.value))
    return TotalSpendingResponse(total_spending=total)


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense_by_id(
    expense_id: int,
    service: ExpenseService = Depends(get_expense_service),
):
    expense = service.get_expense(expense_id)
    if expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return expense


@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    payload: ExpenseUpdate,
    service: ExpenseService = Depends(get_expense_service),
):
    expense = service.update_expense(expense_id=expense_id, payload=payload)
    if expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    service: ExpenseService = Depends(get_expense_service),
):
    deleted = service.delete_expense(expense_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return None
