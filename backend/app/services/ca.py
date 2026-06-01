"""
Service de calcul du Chiffre d'Affaires (CA).

Ce module fournit la logique métier pour calculer le CA
basé sur les transactions de type 'income' sur une période donnée.

Le CA est défini comme la somme des revenus (type='income')
sur une période couvrant start_date à end_date (inclus).
"""
from datetime import date
from sqlalchemy.orm import Session

from app.models.transaction import Transaction


def calculate_ca(db: Session, user_id: str, start_date: date, end_date: date) -> float:
    """
    Calcule le Chiffre d'Affaires (CA) pour un utilisateur sur une période donnée.
    
    Le CA représente la somme de toutes les transactions de type 'income'
    (revenus/entrées) dans la période spécifiée.
    
    Args:
        db: Session de base de données SQLAlchemy
        user_id: ID de l'utilisateur
        start_date: Date de début de la période (inclusive)
        end_date: Date de fin de la période (inclusive)
    
    Returns:
        float: Le montant total du CA pour la période
    
    Example:
        >>> ca = calculate_ca(db, "user-123", date(2024, 1, 1), date(2024, 1, 31))
        >>> print(f"CA Janvier 2024: {ca} XOF")
    """
    result = db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.type == "income",
        Transaction.date >= start_date,
        Transaction.date <= end_date,
    ).with_entities(Transaction.amount).all()
    
    # Utiliser une requête SQL optimisée avec SUM pour les grandes volumes
    # Ici on fait un sum() Python pour la simplicité, mais pour des performances
    # optimales avec des milliers de transactions, on pourrait utiliser:
    # db.query(func.sum(Transaction.amount)).filter(...).scalar() ou None
    
    return sum(row[0] for row in result)


def calculate_ca_aggregate(db: Session, user_id: str, start_date: date, end_date: date) -> dict:
    """
    Calcule le CA avec des métadonnées supplémentaires.
    
    Retourne le CA brut et le nombre de transactions pour une analyse
    plus approfondie.
    
    Args:
        db: Session de base de données SQLAlchemy
        user_id: ID de l'utilisateur
        start_date: Date de début de la période
        end_date: Date de fin de la période
    
    Returns:
        dict:包含了'ca', 'transaction_count'等字段的字典
    """
    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.type == "income",
        Transaction.date >= start_date,
        Transaction.date <= end_date,
    ).all()
    
    return {
        "ca": sum(t.amount for t in transactions),
        "transaction_count": len(transactions),
        "start_date": start_date,
        "end_date": end_date,
    }