"""
Tests d'intégration pour l'endpoint API du CA.

Teste le endpoint /api/ca et ses fonctionnalités.
"""
from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.transaction import Transaction


class TestCAEndpoint:
    """Tests pour l'endpoint GET /api/ca."""

    def test_get_ca_success(
        self, client: TestClient, db: Session, test_user: User, 
        test_transactions: list[Transaction], auth_headers: dict
    ):
        """Test le calcul du CA avec succès."""
        response = client.get(
            "/api/ca",
            params={"start_date": "2024-01-01", "end_date": "2024-12-31"},
            headers=auth_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "ca" in data
        assert "start_date" in data
        assert "end_date" in data
        assert "currency" in data
        assert data["ca"] == 155000.0
        assert data["currency"] == "XOF"

    def test_get_ca_single_month(
        self, client: TestClient, test_user: User, 
        test_transactions: list[Transaction], auth_headers: dict
    ):
        """Test le CA pour un seul mois."""
        response = client.get(
            "/api/ca",
            params={"start_date": "2024-01-01", "end_date": "2024-01-31"},
            headers=auth_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["ca"] == 50000.0

    def test_get_ca_empty_period(
        self, client: TestClient, test_user: User, auth_headers: dict
    ):
        """Test le CA sur une période vide."""
        response = client.get(
            "/api/ca",
            params={"start_date": "2023-01-01", "end_date": "2023-12-31"},
            headers=auth_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["ca"] == 0.0

    def test_get_ca_invalid_dates(
        self, client: TestClient, test_user: User, auth_headers: dict
    ):
        """Test avec des dates invalides (start_date > end_date)."""
        response = client.get(
            "/api/ca",
            params={"start_date": "2024-12-31", "end_date": "2024-01-01"},
            headers=auth_headers,
        )
        
        assert response.status_code == 400
        assert "date de début" in response.json()["detail"].lower()

    def test_get_ca_missing_params(
        self, client: TestClient, auth_headers: dict
    ):
        """Test avec des paramètres manquants."""
        response = client.get(
            "/api/ca",
            headers=auth_headers,
        )
        
        # FastAPI retourne 422 pour les paramètres requis manquants
        assert response.status_code == 422

    def test_get_ca_without_auth(
        self, client: TestClient
    ):
        """Test l'accès sans authentification."""
        response = client.get(
            "/api/ca",
            params={"start_date": "2024-01-01", "end_date": "2024-12-31"},
        )
        
        # Doit retourner 401 Unauthorized
        assert response.status_code == 401

    def test_get_ca_response_format(
        self, client: TestClient, test_user: User, 
        test_transactions: list[Transaction], auth_headers: dict
    ):
        """Test le format de la réponse."""
        response = client.get(
            "/api/ca",
            params={"start_date": "2024-01-01", "end_date": "2024-03-31"},
            headers=auth_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Vérifier les types
        assert isinstance(data["ca"], (int, float))
        assert isinstance(data["start_date"], str)
        assert isinstance(data["end_date"], str)
        assert isinstance(data["currency"], str)
        
        # Vérifier le format des dates (ISO 8601)
        assert data["start_date"] == "2024-01-01"
        assert data["end_date"] == "2024-03-31"


class TestCADetailedEndpoint:
    """Tests pour l'endpoint GET /api/ca/detailed."""

    def test_get_ca_detailed_success(
        self, client: TestClient, test_user: User, 
        test_transactions: list[Transaction], auth_headers: dict
    ):
        """Test le endpoint CA détaillé avec succès."""
        response = client.get(
            "/api/ca/detailed",
            params={"start_date": "2024-01-01", "end_date": "2024-12-31"},
            headers=auth_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["ca"] == 155000.0
        assert data["transaction_count"] == 3
        assert "average_transaction" in data
        assert data["currency"] == "XOF"

    def test_get_ca_detailed_empty_period(
        self, client: TestClient, test_user: User, auth_headers: dict
    ):
        """Test le CA détaillé sur une période vide."""
        response = client.get(
            "/api/ca/detailed",
            params={"start_date": "2023-01-01", "end_date": "2023-12-31"},
            headers=auth_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["ca"] == 0.0
        assert data["transaction_count"] == 0
        assert data["average_transaction"] == 0.0

    def test_get_ca_detailed_average_calculation(
        self, client: TestClient, test_user: User, 
        test_transactions: list[Transaction], auth_headers: dict
    ):
        """Test le calcul de la moyenne."""
        response = client.get(
            "/api/ca/detailed",
            params={"start_date": "2024-02-01", "end_date": "2024-02-29"},
            headers=auth_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # 2 transactions: 75000 + 30000 = 105000
        # Moyenne = 105000 / 2 = 52500
        assert data["ca"] == 105000.0
        assert data["transaction_count"] == 2
        assert data["average_transaction"] == 52500.0


class TestCAEdgeCases:
    """Tests pour les cas limites du CA."""

    def test_ca_with_large_amounts(
        self, client: TestClient, db: Session, test_user: User, auth_headers: dict
    ):
        """Test le CA avec des montants élevés."""
        # Ajouter des transactions avec de gros montants
        for i in range(10):
            txn = Transaction(
                id=f"large-txn-{i}",
                user_id=test_user.id,
                date=date(2024, 5, i + 1),
                type="income",
                amount=10_000_000.0,  # 10 millions
                source="manual",
            )
            db.add(txn)
        db.commit()

        response = client.get(
            "/api/ca",
            params={"start_date": "2024-05-01", "end_date": "2024-05-31"},
            headers=auth_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["ca"] == 100_000_000.0

    def test_ca_decimal_precision(
        self, client: TestClient, db: Session, test_user: User, auth_headers: dict
    ):
        """Test la précision décimale du CA."""
        # Ajouter des transactions avec des décimales
        txn = Transaction(
            id="decimal-txn",
            user_id=test_user.id,
            date=date(2024, 6, 1),
            type="income",
            amount=123.456,
            source="manual",
        )
        db.add(txn)
        db.commit()

        response = client.get(
            "/api/ca",
            params={"start_date": "2024-06-01", "end_date": "2024-06-30"},
            headers=auth_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        # Le CA doit être arrondi à 2 décimales
        assert data["ca"] == 123.46