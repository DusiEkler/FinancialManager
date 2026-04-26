import pytest

from services.ingestion import IngestionService
from unittest.mock import MagicMock, patch
from database.database import db
from schemas.parser_schemas import TransactionOut
from datetime import datetime
from sqlalchemy import select
from database.models import Transaction
from repositories.transaction_repository import TransactionRepository


current_time=datetime.now()

@pytest.fixture(scope='session', autouse=True)
def setup_db():
    base = db.get_base()
    base.metadata.drop_all(db.engine)    
    base.metadata.create_all(db.engine)  
    yield
    base.metadata.drop_all(db.engine)    
    
    
    
@pytest.fixture()
def test_transaction():
    transaction = TransactionOut(
        id = "pedik2006",
        time = current_time,
        amount = 20.0,
        description = "Fitnes center",
        mcc = 900,
        counter_name = "Baloga",
        category = "Sport"
    )
    
    return transaction

@pytest.fixture()
def mock_embbedings():
    session = next(db.get_session())
    ingsetion = IngestionService(session)
    with patch.object(ingsetion, 'client') as mc:
        mock_item = MagicMock()
        mock_item.embedding = [0.1] * 3072
        mock_response = MagicMock()
        mock_response.data = [mock_item]   
        mc.embeddings.create.return_value = mock_response
        yield ingsetion
        


    
def test_ingestion(test_transaction, mock_embbedings):
    mock_embbedings.ingest_transaction([test_transaction])
    st = select(Transaction)
    result = mock_embbedings.db_session.scalars(select(Transaction).where(Transaction.id == test_transaction.id)).first()
    assert result.id == test_transaction.id
     
         
    
    
    

class TestTransaction:
    def test_get_monthly_spending_stats(self, test_transaction, mock_embbedings):
        tr = TransactionRepository(db_session=mock_embbedings.db_session)
        mock_embbedings.ingest_transaction([test_transaction])
        result = tr.get_monthly_spending_stats()
        assert result.first()
    
    def test_search_similar_transactions(self, test_transaction, mock_embbedings):
        tr = TransactionRepository(db_session=mock_embbedings.db_session)
        tr.client = mock_embbedings.client
        mock_embbedings.ingest_transaction([test_transaction])
        result = tr.search_similar_transactions(test_transaction.description)
        assert result.first()
        