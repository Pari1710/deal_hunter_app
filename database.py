# database.py

import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import datetime
import os

# Use an environment variable for the database URL, falling back to local SQLite
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///properties.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Property(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True, index=True)
    scraped_date = Column(DateTime, default=datetime.datetime.utcnow)
    title = Column(String, index=True)
    price_text = Column(String)
    bedrooms = Column(String)
    area_sqft = Column(String)
    price_inr = Column(Float)
    area = Column(Float)
    price_per_sqft = Column(Float)
    noi = Column(Float)
    cap_rate = Column(Float)
    cash_on_cash_return = Column(Float)
    investment_score = Column(Float)

def init_db():
    print("Initializing the database...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")

def save_properties(df: pd.DataFrame):
    print(f"Attempting to save {len(df)} properties to the database...")
    table_columns = [c.name for c in Property.__table__.columns if c.name != 'id']
    df_to_save = df.reindex(columns=table_columns)
    df_to_save.to_sql('properties', con=engine, if_exists='append', index=False)
    print(f"Successfully saved properties to the database.")

def load_all_properties() -> pd.DataFrame:
    print("Loading all historical property data from the database...")
    try:
        df = pd.read_sql_table('properties', con=engine)
        df = df.sort_values(by=['scraped_date', 'investment_score'], ascending=[False, False])
        return df
    except ValueError:
        return pd.DataFrame()