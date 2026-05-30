from datetime import date

from pydantic import BaseModel


class TransactionCreate(BaseModel):
    date: date
    type: str  # "income" or "expense"
    amount: float
    source: str = "manual"
    note: str | None = None


class TransactionResponse(BaseModel):
    id: str
    user_id: str
    date: date
    type: str
    amount: float
    source: str
    note: str | None

    model_config = {"from_attributes": True}


class TransactionListResponse(BaseModel):
    transactions: list[TransactionResponse]
    total: int
