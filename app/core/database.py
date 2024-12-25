from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=5,
    max_overflow=10,
    connect_args={'charset': 'utf8mb4'}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_db_connection():
    try:
        db = SessionLocal()
        result = db.execute("SELECT * FROM provinces LIMIT 1")
        print("Database connection successful")
        print("Sample data:", result.fetchone())
        db.close()
        return True
    except Exception as e:
        print("Database connection failed:", str(e))
        return False 