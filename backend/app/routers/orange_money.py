"""
Orange Money integration router.

This provides the OAuth2 flow stubs for connecting Orange Money accounts.
In production, replace the stub endpoints with real Orange Money API calls.
"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.orange_money import OrangeMoneyAccount
from app.config import ORANGE_MONEY_CLIENT_ID, ORANGE_MONEY_REDIRECT_URI
from app.services.auth import get_current_user

router = APIRouter(prefix="/orange-money", tags=["orange-money"])


@router.get("/auth-url")
def get_auth_url(current_user: User = Depends(get_current_user)):
    if not ORANGE_MONEY_CLIENT_ID:
        return {
            "url": None,
            "message": "Orange Money pas encore configuré. Utilisez la saisie manuelle.",
            "status": "not_configured",
        }
    auth_url = (
        f"https://api.orange.com/oauth/v3/authorize"
        f"?client_id={ORANGE_MONEY_CLIENT_ID}"
        f"&redirect_uri={ORANGE_MONEY_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=read_transactions"
    )
    return {"url": auth_url, "status": "ready"}


@router.post("/callback")
def oauth_callback(
    code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # In production: exchange code for access token via Orange Money API
    # For MVP stub, we simulate the connection
    account = db.query(OrangeMoneyAccount).filter(
        OrangeMoneyAccount.user_id == current_user.id
    ).first()

    if not account:
        account = OrangeMoneyAccount(
            user_id=current_user.id,
            encrypted_token=f"stub_token_{code}",
            last_sync=datetime.utcnow(),
            balance=0.0,
        )
        db.add(account)
    else:
        account.encrypted_token = f"stub_token_{code}"
        account.last_sync = datetime.utcnow()

    db.commit()
    return {"status": "connected", "message": "Orange Money connecté avec succès"}


@router.get("/status")
def get_om_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = db.query(OrangeMoneyAccount).filter(
        OrangeMoneyAccount.user_id == current_user.id
    ).first()

    if not account:
        return {"connected": False, "last_sync": None, "balance": 0}

    return {
        "connected": True,
        "last_sync": account.last_sync.isoformat() if account.last_sync else None,
        "balance": account.balance,
    }


@router.post("/sync")
def sync_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = db.query(OrangeMoneyAccount).filter(
        OrangeMoneyAccount.user_id == current_user.id
    ).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Orange Money non connecté",
        )

    # In production: fetch transactions from Orange Money API
    # and insert/merge into transactions table
    account.last_sync = datetime.utcnow()
    db.commit()

    return {
        "status": "synced",
        "message": "Synchronisation effectuée",
        "last_sync": account.last_sync.isoformat(),
    }
