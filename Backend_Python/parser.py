from models import ParsedTransaction, TransactionOut
import json
from categorizer import get_category

def convert_csv_to_json():
    pass

def parse_monobank_statement(_data: str) -> list:
    data = json.loads(_data)

    transactions = []

    for transaction in data:
        parsed_transaction = ParsedTransaction(**transaction)
        _category = get_category(parsed_transaction.mcc, parsed_transaction.description)

        transactions.append(TransactionOut(
            **transaction,
            category = _category
        )) 

    return transactions       

with open("transactions.json", "r") as file:
    data = file.read()
    print(parse_monobank_statement(data))
