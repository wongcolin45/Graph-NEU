from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# Replace with your actual credentials
DATABASE_URL = "postgresql+psycopg2://colin:barkley@localhost:5432/coursesDB"

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a scoped session factory
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))
