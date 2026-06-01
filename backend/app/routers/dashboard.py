from datetime import date, timedelta
from collections import defaultdict

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.transaction import Transaction
from app.schemas.dashboard import DashboardResponse, DailyFlow, UserProfileUpdate
from app.services.auth import get_current_user
from app.services.forecast import compute_forecast
from app.services.ca import calculate_ca

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardResponse)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    today = date.today()
    thirty_days_ago = today - timedelta(days=30)
    week_start = today - timedelta(days=today.weekday())

    all_txns = (
        db.query(Transaction)
        .filter(
            Transaction.user_id == current_user.id,
            Transaction.date >= thirty_days_ago,
        )
        .order_by(Transaction.date)
        .all()
    )

    total_income = sum(t.amount for t in all_txns if t.type == "income")
    total_expense = sum(t.amount for t in all_txns if t.type == "expense")
    current_balance = total_income - total_expense

    week_txns = [t for t in all_txns if t.date >= week_start]
    weekly_income = sum(t.amount for t in week_txns if t.type == "income")
    weekly_expense = sum(t.amount for t in week_txns if t.type == "expense")

    daily_map: dict[date, dict[str, float]] = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
    for t in all_txns:
        if t.date >= today - timedelta(days=7):
            daily_map[t.date][t.type] += t.amount

    daily_flows = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        inc = daily_map[d]["income"]
        exp = daily_map[d]["expense"]
        daily_flows.append(DailyFlow(date=d, income=inc, expense=exp, net=inc - exp))

    txn_dicts = [
        {"date": t.date, "type": t.type, "amount": t.amount}
        for t in all_txns
    ]
    forecast_points, risk_level, alerts = compute_forecast(txn_dicts, current_balance)

    return DashboardResponse(
        current_balance=round(current_balance, 0),
        weekly_income=round(weekly_income, 0),
        weekly_expense=round(weekly_expense, 0),
        weekly_net=round(weekly_income - weekly_expense, 0),
        forecast_15d=forecast_points,
        risk_level=risk_level,
        alerts=alerts,
        daily_flows_7d=daily_flows,
        currency=current_user.currency,
        # Chiffre d'Affaires = total des revenus sur la période (30 jours)
        chiffre_affaires=round(total_income, 0),
    )


@router.put("/profile")
def update_profile(
    data: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if data.name is not None:
        current_user.name = data.name
    if data.sector is not None:
        current_user.sector = data.sector
    if data.currency is not None:
        current_user.currency = data.currency
    db.commit()
    return {"status": "ok", "message": "Profil mis à jour"}
