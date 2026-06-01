"""
Tests unitaires pour le service de calcul du CA.

Teste la logique métier de calcul du Chiffre d'Affaires.
"""
from datetime import date

import pytest
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.transaction import Transaction
from app.services.ca import calculate_ca, calculate_ca_aggregate


class TestCalculateCA:
    """Tests pour la fonction calculate_ca."""

    def test_calculate_ca_with_income_transactions(
        self, db: Session, test_user: User, test_transactions: list[Transaction]
    ):
        """Test le calcul du CA avec des transactions de revenus."""
        ca = calculate_ca(db, test_user.id, date(2024, 1, 1), date(2024, 12, 31))
        
        # Les revenus sont: 50000 + 75000 + 30000 = 155000
        assert ca == 155000.0

    def test_calculate_ca_empty_period(
        self, db: Session, test_user: User
    ):
        """Test le calcul du CA sur une période sans transactions."""
        ca = calculate_ca(db, test_user.id, date(2023, 1, 1), date(2023, 12, 31))
        
        assert ca == 0.0

    def test_calculate_ca_single_month(
        self, db: Session, test_user: User, test_transactions: list[Transaction]
    ):
        """Test le calcul du CA pour un seul mois."""
        ca = calculate_ca(db, test_user.id, date(2024, 1, 1), date(2024, 1, 31))
        
        # Seul revenu en janvier: 50000
        assert ca == 50000.0

    def test_calculate_ca_excludes_expenses(
        self, db: Session, test_user: User, test_transactions: list[Transaction]
    ):
        """Test que les dépenses ne sont pas incluses dans le CA."""
        ca = calculate_ca(db, test_user.id, date(2024, 1, 1), date(2024, 3, 31))
        
        # Revenus uniquement: 50000 + 75000 + 30000 = 155000
        # Les dépenses (20000 + 15000) sont exclues
        assert ca == 155000.0

    def test_calculate_ca_february_only(
        self, db: Session, test_user: User, test_transactions: list[Transaction]
    ):
        """Test le calcul du CA pour février uniquement."""
        ca = calculate_ca(db, test_user.id, date(2024, 2, 1), date(2024, 2, 29))
        
        # Revenus février: 75000 + 30000 = 105000
        assert ca == 105000.0

    def test_calculate_ca_nonexistent_user(
        self, db: Session
    ):
        """Test le calcul du CA pour un utilisateur inexistant."""
        ca = calculate_ca(db, "nonexistent-user-id", date(2024, 1, 1), date(2024, 12, 31))
        
        assert ca == 0.0

    def test_calculate_ca_boundary_dates(
        self, db: Session, test_user: User, test_transactions: list[Transaction]
    ):
        """Test le calcul du CA avec des dates limites."""
        # Test avec la date exacte d'une transaction
        ca = calculate_ca(db, test_user.id, date(2024, 1, 15), date(2024, 1, 15))
        
        # Un seul revenu à cette date: 50000
        assert ca == 50000.0

    def test_calculate_ca_decimal_amounts(
        self, db: Session, test_user: User
    ):
        """Test le calcul du CA avec des montants décimaux."""
        # Ajouter des transactions avec montants décimaux
        transactions = [
            Transaction(
                id="txn-decimal-1",
                user_id=test_user.id,
                date=date(2024, 4, 1),
                type="income",
                amount=12345.67,
                source="manual",
            ),
            Transaction(
                id="txn-decimal-2",
                user_id=test_user.id,
                date=date(2024, 4, 2),
                type="income",
                amount=9876.54,
                source="manual",
            ),
        ]
        for txn in transactions:
            db.add(txn)
        db.commit()

        ca = calculate_ca(db, test_user.id, date(2024, 4, 1), date(2024, 4, 30))
        
        # Somme: 12345.67 + 9876.54 = 22222.21
        assert ca == 22222.21


class TestCalculateCAAggregate:
    """Tests pour la fonction calculate_ca_aggregate."""

    def test_aggregate_returns_all_fields(
        self, db: Session, test_user: User, test_transactions: list[Transaction]
    ):
        """Test que l'agrégat retourne tous les champs."""
        result = calculate_ca_aggregate(
            db, test_user.id, date(2024, 1, 1), date(2024, 12, 31)
        )
        
        assert "ca" in result
        assert "transaction_count" in result
        assert "start_date" in result
        assert "end_date" in result
        assert result["ca"] == 155000.0
        assert result["transaction_count"] == 3  # 3 transactions de type income

    def test_aggregate_empty_period(
        self, db: Session, test_user: User
    ):
        """Test l'agrégat sur une période vide."""
        result = calculate_ca_aggregate(
            db, test_user.id, date(2023, 1, 1), date(2023, 12, 31)
        )
        
        assert result["ca"] == 0.0
        assert result["transaction_count"] == 0

    def test_aggregate_correct_count(
        self, db: Session, test_user: User, test_transactions: list[Transaction]
    ):
        """Test que le comptage des transactions est correct."""
        result = calculate_ca_aggregate(
            db, test_user.id, date(2024, 2, 1), date(2024, 2, 29)
        )
        
        # 2 revenus en février
        assert result["transaction_count"] == 2