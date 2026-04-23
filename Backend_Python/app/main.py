from fastapi import FastAPI, Depends
from app.services.parser import parse_monobank_statement
from sqlalchemy.orm import Session
from app.database.database import db
from app.services.ingestion import IngestionService

app = FastAPI()

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.post("/transactions/upload")
async def upload_transactions(transactions_data: list[dict], session: Session = Depends(db.get_session)):
    transaciton_out_list = parse_monobank_statement(transactions_data)
    ingestion_service = IngestionService(session)
    ingestion_service.ingest_transaction(transaciton_out_list)

    return {"status": "success", "parsed_count": len(transaciton_out_list)}