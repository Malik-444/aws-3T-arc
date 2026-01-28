# main.py


from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import os


# Database connection

# Using environment variables is industry-standard for credentials
DB_USER = os.getenv("DB_USER", "postgres")  # RDS username
DB_PASS = os.getenv("DB_PASS", "YourPassword")  # RDS password
DB_NAME = os.getenv("DB_NAME", "todosdb")  # Database name
DB_HOST = os.getenv("DB_HOST", "your-db-endpoint.rds.amazonaws.com")  # RDS endpoint
DB_PORT = os.getenv("DB_PORT", "5432")  # PostgreSQL default port

# Full PostgreSQL connection URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy engine handles connection pooling
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# SessionLocal factory creates a DB session per request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()


# 2️ Database model

class Todo(Base):
    __tablename__ = "todos"  # Table name in RDS
    id = Column(Integer, primary_key=True, index=True)  # Auto-increment ID
    title = Column(String, nullable=False)  # Todo text

# Create table if it doesn't exist yet
Base.metadata.create_all(bind=engine)


# 3️⃣ Pydantic models (JSON validation)

class TodoRequest(BaseModel):
    title: str  # Expect JSON {"title": "Some task"}

class TodoResponse(BaseModel):
    id: int  # Database-assigned ID
    title: str


#  FastAPI app instance

app = FastAPI()


# 5️⃣ Root endpoint for health check

@app.get("/")
def root():
    """
    Health check endpoint
    Can be used by ALB to verify EC2 is healthy
    """
    return {"message": "Welcome to your FastAPI 3-tier app!"}


#  POST /todos endpoint

@app.post("/todos", response_model=TodoResponse)
def create_todo(todo: TodoRequest):
    """
    Creates a new todo in RDS
    Industry-standard JSON body input:
    {
        "title": "Learn AWS"
    }
    """
    db: Session = SessionLocal()  # Open a new DB session
    new_todo = Todo(title=todo.title)  # Create ORM object
    db.add(new_todo)  # Stage insert
    db.commit()  # Write to database
    db.refresh(new_todo)  # Refresh to get DB-generated ID
    db.close()  # Close session
    return new_todo  # Automatically converted to JSON via TodoResponse


#  GET /todos endpoint

@app.get("/todos", response_model=list[TodoResponse])
def get_todos():
    """
    Returns all todos from RDS
    Safe and stateless, ideal for multi-user cloud app
    """
    db: Session = SessionLocal()
    todos = db.query(Todo).all()  # Fetch all rows
    db.close()
    return todos


# Notes for deployment:
# 1. Run on EC2 in private subnet behind ALB
# 2. Install dependencies: fastapi, uvicorn, sqlalchemy, psycopg2-binary
# 3. Run server: python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
# 4. Use curl to test via ALB
# 5. Keep DB credentials in environment variables

