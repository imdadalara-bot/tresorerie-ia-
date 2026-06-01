"""
Router pour le Chiffre d'Affaires (CA).

Expose les endpoints API pour le calcul et la récupération du CA.
"""
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.ca import CAResponse, CADetailedResponse
from app.services.auth import get_current_user
from app.services.ca import calculate_ca, calculate_ca_aggregate

router = APIRouter(prefix="/ca", tags=["chiffre-d-affaires"])


@router.get(
    "",
    response_model=CAResponse,
    summary="Obtenir le Chiffre d'Affaires",
    description="""
    Calcule et retourne le Chiffre d'Affaires (CA) pour la période spécifiée.
    
    Le CA est calculé comme la somme de toutes les transactions de type 'income'
    (revenus/entrées) sur la période définie par start_date et end_date.
    
    **Paramètres:**
    - `start_date`: Date de début (format YYYY-MM-DD)
    - `end_date`: Date de fin (format YYYY-MM-DD)
    
    **Note:** Les dates doivent être valides et start_date doit être <= end_date.
    """,
)
def get_ca(
    start_date: date = Query(
        ...,
        description="Date de début de la période (YYYY-MM-DD)",
        examples=["2024-01-01"],
    ),
    end_date: date = Query(
        ...,
        description="Date de fin de la période (YYYY-MM-DD)",
        examples=["2024-12-31"],
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Récupère le CA pour la période spécifiée.
    
    Args:
        start_date: Date de début de la période
        end_date: Date de fin de la période
        db: Session de base de données
        current_user: Utilisateur authentifié
    
    Returns:
        CAResponse: Le CA calculé avec les dates et la devise
    
    Raises:
        HTTPException: Si les dates sont invalides ou si start_date > end_date
    """
    if start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="La date de début doit être antérieure ou égale à la date de fin"
        )
    
    ca = calculate_ca(db, current_user.id, start_date, end_date)
    
    return CAResponse(
        ca=round(ca, 2),
        start_date=start_date,
        end_date=end_date,
        currency=current_user.currency,
    )


@router.get(
    "/detailed",
    response_model=CADetailedResponse,
    summary="Obtenir le CA avec détails",
    description="""
    Retourne le Chiffre d'Affaires avec des métadonnées supplémentaires:
    - Nombre de transactions de revenus
    - Montant moyen par transaction
    
    Utile pour une analyse plus approfondie des revenus.
    """,
)
def get_ca_detailed(
    start_date: date = Query(
        ...,
        description="Date de début de la période (YYYY-MM-DD)",
        examples=["2024-01-01"],
    ),
    end_date: date = Query(
        ...,
        description="Date de fin de la période (YYYY-MM-DD)",
        examples=["2024-12-31"],
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Récupère le CA détaillé avec métadonnées.
    
    Args:
        start_date: Date de début de la période
        end_date: Date de fin de la période
        db: Session de base de données
        current_user: Utilisateur authentifié
    
    Returns:
        CADetailedResponse: Le CA avec détails additionnels
    """
    if start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="La date de début doit être antérieure ou égale à la date de fin"
        )
    
    result = calculate_ca_aggregate(db, current_user.id, start_date, end_date)
    avg = result["ca"] / result["transaction_count"] if result["transaction_count"] > 0 else 0.0
    
    return CADetailedResponse(
        ca=round(result["ca"], 2),
        start_date=start_date,
        end_date=end_date,
        currency=current_user.currency,
        transaction_count=result["transaction_count"],
        average_transaction=round(avg, 2),
    )