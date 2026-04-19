from schemas.transaction import TransactionSchema
from database.models import Transaction, TransactionEmbedding
from openai import OpenAI


class IngestionService:
    def __init__(self, db_session):
        self.db_session = db_session
    
    def ingest_transaction(self, schema: TransactionSchema):
        transaction = Transaction(
            id=schema.id, 
            time=schema.time, 
            amount=schema.amount, 
            description=schema.description,
            mcc=schema.mcc,
            counter_name=schema.counter_name,
            category=schema.category
            )
        client = OpenAI()
        response = client.embeddings.create(
        input=f"{schema.description}",
        model="text-embedding-3-small"
        )
        transaction_embedding = TransactionEmbedding(transaction_id=schema.id, 
                                                     embedding=response.data[0].embedding)
        with self.db_session as session:
            session.add(transaction)
            session.add(transaction_embedding)
            session.commit()
        
        
    