from sqlalchemy import func, extract, select
from database.models import Transaction, TransactionEmbedding
from datetime import datetime
from openai import OpenAI


class TransactionRepository:
    def __init__(self, db_session):
        self.session = db_session
        
    def get_monthly_spending_stats(self):
        now = datetime.now()
        return self.session.query(Transaction.time,
                                  func.sum(Transaction.amount).label('total')
                                 ).filter(extract('month', Transaction.time) == now.month,extract('year', Transaction.time) == now.year).group_by(Transaction.category)
    
    def search_similar_transactions(self, query: str, limit: int = 5):
        client = OpenAI()
        response = client.embeddings.create(
        input=f"{query}",
        model="text-embedding-3-small"
        )
        return self.session.scalars(select(TransactionEmbedding).order_by(TransactionEmbedding.embedding.cosine_distance(response.data[0].embedding)).limit(limit))
    
