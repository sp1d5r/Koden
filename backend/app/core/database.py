from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.engine import Engine
from sqlalchemy.pool import StaticPool
import os
from dotenv import load_dotenv
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Import models
from db.models.base import SQLModel

load_dotenv()

def get_database_url() -> str:
    """Get database URL based on environment."""
    env = os.getenv("ENV", "development")
    
    if env == "development":
        # Development database URL
        return os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:postgres@localhost:5432/dev_db"
        )
    else:
        # Deployment database URL
        return os.getenv("DATABASE_URL")
        

DATABASE_URL = get_database_url()

engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("ENV", "development") == "development",  # Only echo SQL in development
    pool_pre_ping=True,
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    with Session(engine) as session:
        yield session 