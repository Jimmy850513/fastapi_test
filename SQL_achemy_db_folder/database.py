from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



sql_connect_url = f"""postgresql+psycopg2://jimmy:home1234@localhost:5432/fast_api_test"""
        
engine = create_engine(sql_connect_url)
            
SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)

Base = declarative_base()
           
def get_db():
    db =SessionLocal()
    try:
        yield db
    finally:
        db.close() 
