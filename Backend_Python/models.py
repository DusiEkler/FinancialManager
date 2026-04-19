from pydantic import BaseModel, ValidationError, field_validator
from datetime import datetime

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

    @field_validator('amount', mode='after')
    @classmethod
    def to_float_amount(cls, value: int) -> float:
        return float(value/100)

    @field_validator('time', mode='before')
    @classmethod
    def timestamp_to_datetime(cls, value: int) -> datetime:
        return datetime.fromtimestamp(value)

    