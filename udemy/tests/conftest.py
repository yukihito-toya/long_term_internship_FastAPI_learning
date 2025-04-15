import os
import sys
appdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(appdir)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker, Session
from models import Base, User, Item
from modules.m1744258408460 import TokenData
from app_1744251140387 import app
from engine_1744264596580 import get_db
from modules.m1744270065338 import get_current_user

@pytest.fixture()
def session_fixture():
    """
    Fixture to create a database session.
    """
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Create a sample user
        # user = User(username="testuser", password="testpassword", salt="testsalt")
        # db.add(user)
        # db.commit()
        # Create a sample item
        item = Item(name="testitem", price=100, description="testdescription", user_id=1)
        item2 = Item(name="testitem2", price=200, description="testdescription2", user_id=2)
        db.add(item)
        db.add(item2)
        db.commit()
        yield db
    finally:
        db.close()

@pytest.fixture()
def user_fixture():
    """
    Fixture to create a tokendata.
    """
    return TokenData(
        username="testuser",
        user_id=1,
    )

@pytest.fixture()
def use_fixture(session_fixture: Session, user_fixture: TokenData):
    """
    Fixture to create a database session.
    """
    def override_get_db():
        return session_fixture
    def override_get_user():
        return user_fixture
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_user

    client = TestClient(app)
    yield client
    
    app.dependency_overrides.clear()