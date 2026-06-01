"""
Schémas Pydantic pour le Chiffre d'Affaires (CA).

Définit les modèles de données pour les requêtes et réponses
liées au calcul du CA.
"""
from datetime import date

from pydantic import BaseModel, Field


class CARequest(BaseModel):
    """Paramètres de requête pour le calcul du CA."""
    start_date: date = Field(..., description="Date de début de la période (inclusive)")
    end_date: date = Field(..., description="Date de fin de la période (inclusive)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "start_date": "2024-01-01",
                "end_date": "2024-12-31"
            }
        }
    }


class CAResponse(BaseModel):
    """Réponse contenant le Chiffre d'Affaires calculé."""
    ca: float = Field(..., description="Montant total du CA pour la période (somme des revenus)")
    start_date: date = Field(..., description="Date de début de la période")
    end_date: date = Field(..., description="Date de fin de la période")
    currency: str = Field(..., description="Devise utilisée")

    model_config = {"from_attributes": True}


class CADetailedResponse(BaseModel):
    """Réponse détaillée avec métadonnées supplémentaires."""
    ca: float = Field(..., description="Montant total du CA")
    start_date: date
    end_date: date
    currency: str
    transaction_count: int = Field(..., description="Nombre de transactions de revenus sur la période")
    average_transaction: float = Field(..., description="Montant moyen par transaction")

    model_config = {"from_attributes": True}