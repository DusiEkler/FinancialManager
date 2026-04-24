from sqlalchemy import func, extract, select
from database.models import Transaction, TransactionEmbedding
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()


class TransactionRepository:
    def __init__(self, db_session):
        self.session = db_session
        self.client = OpenAI(api_key=os.getenv('API_KEY'),
                             base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
        
    def get_monthly_spending_stats(self):
        now = datetime.now()
        return self.session.query(Transaction.category,
                                  func.sum(Transaction.amount).label('total')
                                 ).filter(extract('month', Transaction.time) == now.month,extract('year', Transaction.time) == now.year).group_by(Transaction.category)
    
    def search_similar_transactions(self, query: str, limit: int = 5):
        
        response = self.client.embeddings.create(
        input=f"{query}",
        model="gemini-embedding-001"
        )
        return self.session.scalars(select(Transaction).join(TransactionEmbedding).order_by(TransactionEmbedding.embedding.cosine_distance(response.data[0].embedding)).limit(limit))
    
    def get_spending_by_category_and_month(self, category, month: int = None, year: int = None):
        now = datetime.now()
        month = month or now.month
        year = year or now.year
        return self.session.query(Transaction.category,
                                  func.sum(Transaction.amount).label('total')
                                 ).filter(extract('month', Transaction.time) == month,
                                          extract('year', Transaction.time) == year
                                          ).filter(Transaction.category == category).group_by(Transaction.category)
    
