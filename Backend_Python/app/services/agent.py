from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
from repositories.transaction_repository import TransactionRepository
import json


class AgentService:
    def __init__(self, db_session):
        self.client = OpenAI(api_key=os.getenv('API_KEY'),
                             base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
        self.tools = [
            {
                "type": "function",
                "name": "get_monthly_spending_stats",
                "description" : "Returns expenses for the month"
            },
            
            {
                "type": "function",
                "name": "search_similar_transactions",
                "description" : "Searches for similar transactions based on the description ",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Specifies the introductory text for the function"
                        },
                        "limit": {
                            "type": "integer", 
                            "description": "Specifies the row limit for a database query"
                        }
                    },
                    "required": ["query"]  
                }
            },
            {
                "type": "function",
                "name": "get_spending_by_category_and_month",
                "description": "Returns expenses for the month filtered by category",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "description": "Specifies the category for the function"
                        },
                        "month": {
                            "type": "integer", 
                            "description": "Specifies the month for the function"
                        },
                        "year": {
                            "type": "integer",
                            "description": "Specifies the year for the function"
                        }
                    },
                    "required": ["category"]  
                }
                
            }
                      ]
        self.transaction = TransactionRepository(db_session=db_session)
        

    def chat(self, user_message: str):
        input_list = [
            {"role": "user", "content": f"{user_message}"}
        ]
        
        response = self.client.responses.create(
        model="gemini-2.5-flash",
        tools=self.tools,
        input=input_list,
        )
        
        input_list += response.output

        for item in response.output:
            if item.type == "function_call":
                if item.name == "get_monthly_spending_stats":
                    get_monthly_spending_stats = self.transaction.get_monthly_spending_stats()
                    input_list.append({
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": str(get_monthly_spending_stats),
                    })
            
            
                elif item.name == "search_similar_transactions":
                    query = json.loads(item.arguments)["query"]
                    search_similar_transactions = self.transaction.search_similar_transactions(query)
                    input_list.append({
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": str(search_similar_transactions),
                    })
                
                elif item.name == "get_spending_by_category_and_month":
                    query = json.loads(item.arguments)
                    get_spending_by_category_and_month = self.transaction.get_spending_by_category_and_month(
                                                                            category=query.get("category"),
                                                                            month=query.get("month"),
                                                                            year=query.get("year")
                                                                            )
                    input_list.append({
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": str(get_spending_by_category_and_month),
                    })
                    
        response = self.client.responses.create(
        model="gemini-2.5-flash",
        tools=self.tools,
        input=input_list,
        )           
        
        for item in response.output:
            if item.type == "text":
                return item.text