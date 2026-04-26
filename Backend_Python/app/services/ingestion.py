from schemas.parser_schemas import TransactionOut
from database.models import Transaction, TransactionEmbedding
from openai import OpenAI
from sqlalchemy.dialects.postgresql import insert
import os
from dotenv import load_dotenv
load_dotenv()



class IngestionService:
    def __init__(self, db_session):
        self.db_session = db_session
        self.client = OpenAI(api_key=os.getenv('API_KEY'),
                             base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
    
    def ingest_transaction(self, schema: list[TransactionOut]):
        descriptions_list = []
        dumped_transactions = []

        for _transaction in schema:
            descriptions_list.append(_transaction.description)
            dumped_transactions.append(_transaction.model_dump())

        transaction = insert(Transaction).values(dumped_transactions).on_conflict_do_nothing(index_elements=['id'])
        
        response = self.client.embeddings.create(
        input=descriptions_list,
        model="gemini-embedding-001"
        )
        
        print(response.data)
        embeddings_list = []
        for i, _transaction in enumerate(response.data):
            embeddings_list.append({
                'transaction_id': schema[i].id,
                'embedding': _transaction.embedding
                
            })
        
        transaction_embedding = insert(TransactionEmbedding).values(embeddings_list).on_conflict_do_nothing(index_elements=['id'])
        with self.db_session as session:
            session.execute(transaction)
            session.execute(transaction_embedding)
            session.commit()