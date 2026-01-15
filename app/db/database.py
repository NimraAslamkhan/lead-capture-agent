from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import DATABASE_URL, SQLALCHEMY_ECHO
from app.db.models import Base

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=SQLALCHEMY_ECHO,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("[OK] Database tables created successfully")


def close_db():
    """Close all database connections"""
    engine.dispose()
