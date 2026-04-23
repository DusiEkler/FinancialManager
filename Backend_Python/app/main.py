from fastapi import FastAPI
from app.services.parser import parse_monobank_statement

app = FastAPI()

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.post("/transactions/upload")
async def upload_transactions(transactions_data: list[dict]):
    count = len(parse_monobank_statement(transactions_data))
    return {"parsed_count": count}