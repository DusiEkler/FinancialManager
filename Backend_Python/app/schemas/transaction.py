from pydantic import BaseModel

from datetime import datetime

class TransactionSchema(BaseModel):
    id: str
    time: datetime
    amount: float
    description: str
    mcc: int
    counter_name: str
    category: str
    
    