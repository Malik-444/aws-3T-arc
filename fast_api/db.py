from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://<USERNAME>:<PASSWORD>@<ENDPOINT>:5432/<DB_NAME>"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
