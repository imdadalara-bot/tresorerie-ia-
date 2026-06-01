from datetime import date

from pydantic import BaseModel, Field


class DailyFlow(BaseModel):
    date: date
    income: float
    expense: float
    net: float


class ForecastPoint(BaseModel):
    date: date
    predicted_balance: float
    confidence: float


class AlertInfo(BaseModel):
    type: str
    message: str
    days_until: int | None = None
    predicted_shortfall: float | None = None


class DashboardResponse(BaseModel):
    current_balance: float
    weekly_income: float
    weekly_expense: float
    weekly_net: float
    forecast_15d: list[ForecastPoint]
    risk_level: str  # LOW, MEDIUM, HIGH
    alerts: list[AlertInfo]
    daily_flows_7d: list[DailyFlow]
    currency: str
    # Chiffre d'Affaires sur la période des 30 derniers jours
    chiffre_affaires: float = Field(
        default=0.0,
        description="Chiffre d'Affaires (somme des revenus) sur la période des 30 derniers jours"
    )


class UserProfileUpdate(BaseModel):
    name: str | None = None
    sector: str | None = None
    currency: str | None = None
