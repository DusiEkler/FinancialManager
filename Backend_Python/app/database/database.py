from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from dotenv import load_dotenv
load_dotenv()
 


class Base(DeclarativeBase):
    pass


class Database:
    def __init__(self, database_url):
        self.database_url = database_url
        self.engine = create_engine(database_url)
        self.session = sessionmaker(self.engine, autocommit=False, autoflush=False)
    
    def get_session(self):
        db = self.session()
        try:
            yield db  # ← передаємо сесію назовні
        finally:
            db.close()
    
    def get_base(self):
        return Base

db = Database(os.getenv("DATABASE_URL"))