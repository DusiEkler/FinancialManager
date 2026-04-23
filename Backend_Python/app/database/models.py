from app.database.database import db
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy import String, Float, Integer, DateTime
from datetime import datetime
from sqlalchemy import ForeignKey
from pgvector.sqlalchemy import Vector

base = db.get_base()

class Transaction(base):
    __tablename__ = "transaction"
    id: Mapped[str] = mapped_column(String(30), primary_key = True)
    time: Mapped[datetime] = mapped_column(DateTime) 
    amount: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(String(100))
    mcc: Mapped[int] = mapped_column(Integer)
    counter_name: Mapped[str] = mapped_column(String(30))
    category: Mapped[str] = mapped_column(String(30))

class TransactionEmbedding(base):
    __tablename__ = "transaction_embedding"
    id: Mapped[int] = mapped_column(primary_key = True, autoincrement=True)
    transaction_id: Mapped[str] = mapped_column(ForeignKey("transaction.id"))
    embedding: Mapped[Vector] = mapped_column(Vector(1536))