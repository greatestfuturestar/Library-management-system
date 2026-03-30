import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.database import Base
from app.models import book, book_copy, user, borrow_record

# In-memory SQLite — fast, disposable, no touching library.db
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

@pytest.fixture(scope="function")
def db():
    # Create all tables fresh before each test
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Wipe all tables after each test — clean slate
        Base.metadata.drop_all(bind=engine)