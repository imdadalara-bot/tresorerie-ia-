"""
Configuration des tests pytest.

Fournit les fixtures pour les tests du backend Trésorier IA.
"""
import uuid
from datetime import date, datetime
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.database import Base, get_db
from app.models.user import User
from app.models.transaction import Transaction
from app.main import app

# Base de données SQLite en mémoire pour les tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db() -> Generator[Session, None, None]:
    """Override de la dépendance get_db pour les tests."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """Fixture de session de base de données pour les tests."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Session) -> TestClient:
    """Fixture de client de test FastAPI."""
    return TestClient(app)


@pytest.fixture
def test_user(db: Session) -> User:
    """Crée un utilisateur de test."""
    user = User(
        id=str(uuid.uuid4()),
        email="test@example.com",
        hashed_password="$2b$12$test_hash",
        name="Test User",
        sector="commerce",
        currency="XOF",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_transactions(db: Session, test_user: User) -> list[Transaction]:
    """Crée des transactions de test."""
    transactions = [
        Transaction(
            id=str(uuid.uuid4()),
            user_id=test_user.id,
            date=date(2024, 1, 15),
            type="income",
            amount=50000.0,
            source="manual",
            note="Vente produit A",
        ),
        Transaction(
            id=str(uuid.uuid4()),
            user_id=test_user.id,
            date=date(2024, 1, 20),
            type="expense",
            amount=20000.0,
            source="manual",
            note="Achat fournitures",
        ),
        Transaction(
            id=str(uuid.uuid4()),
            user_id=test_user.id,
            date=date(2024, 2, 10),
            type="income",
            amount=75000.0,
            source="manual",
            note="Prestation service",
        ),
        Transaction(
            id=str(uuid.uuid4()),
            user_id=test_user.id,
            date=date(2024, 2, 15),
            type="income",
            amount=30000.0,
            source="manual",
            note="Consultation",
        ),
        Transaction(
            id=str(uuid.uuid4()),
            user_id=test_user.id,
            date=date(2024, 3, 1),
            type="expense",
            amount=15000.0,
            source="manual",
            note="Loyer",
        ),
    ]
    for txn in transactions:
        db.add(txn)
    db.commit()
    return transactions


@pytest.fixture
def auth_token(test_user: User) -> str:
    """
    Génère un token JWT simulé pour les tests.
    Note: En conditions réelles, on utiliserait le vrai mécanisme d'auth.
    """
    from jose import jwt
    from app.config import SECRET_KEY, ALGORITHM
    
    # Utiliser les mêmes clés que l'app
    return jwt.encode(
        {"sub": test_user.id, "email": test_user.email},
        SECRET_KEY,
        algorithm=ALGORITHM
    )


@pytest.fixture
def auth_headers(auth_token: str) -> dict:
    """Headers d'authentification pour les requêtes API."""
    return {"Authorization": f"Bearer {auth_token}"}