from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from dotenv import load_dotenv
import os
load_dotenv()  # looks for .env up the directory tree

URL = (
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT','5432')}/{os.getenv('POSTGRES_DB')}"
)
engine = create_engine(URL, pool_pre_ping=True)

# Create a scoped session factory
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))
