from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# O host 'db' refere-se ao nome do serviço no docker-compose
SQLALCHEMY_DATABASE_URL = "postgresql://admin:password@db:5432/streaming_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()