from pydantic import BaseModel, ValidationError, field_validator
from datetime import datetime
from typing import Any

class ParsedTransaction(BaseModel):
    id: str
    time: int
    amount: int
    description: str
    mcc: int
    counterName: str

class TransactionOut(BaseModel):
    id: str
    time: datetime
    amount: float
    description: str
    mcc: int
    counterName: str
    category: str

    @field_validator('amount', mode='before')
    @classmethod
    def to_float_amount(cls, value: Any) -> float:
        if isinstance(value, int):
            return value / 100.0
        return value

    @field_validator('time', mode='before')
    @classmethod
    def timestamp_to_datetime(cls, value: Any) -> datetime:
        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(value)
        return value

    