from schemas.transaction import TransactionSchema
from database.models import Transaction, TransactionEmbedding
from openai import OpenAI
from sqlalchemy.dialects.postgresql import insert


class IngestionService:
    def __init__(self, db_session):
        self.db_session = db_session
        self.client = OpenAI()
    
    def ingest_transaction(self, schema: TransactionSchema):
        transaction = insert(Transaction).values(
            id=schema.id, 
            time=schema.time, 
            amount=schema.amount, 
            description=schema.description,
            mcc=schema.mcc,
            counter_name=schema.counter_name,
            category=schema.category
            ).on_conflict_do_nothing(index_elements=['id'])
        
        response = self.client.embeddings.create(
        input=f"{schema.description}",
        model="text-embedding-3-small"
        )
        transaction_embedding = insert(TransactionEmbedding).values(transaction_id=schema.id, 
                                                     embedding=response.data[0].embedding
                                                     ).on_conflict_do_nothing(index_elements=['id'])
        with self.db_session as session:
            session.execute(transaction)
            session.execute(transaction_embedding)
            session.commit()