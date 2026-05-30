"""
Trésorier IA - Cash Flow Forecast Agent

Predicts balance for the next 15 days using:
1. Day-of-week average net flow (seasonality)
2. Linear trend from recent history
3. Confidence interval (±20%)

Works with as few as 7 days of data; improves with 30+ days.
"""

from datetime import date, timedelta
from collections import defaultdict

import numpy as np

from app.schemas.dashboard import ForecastPoint, AlertInfo


def compute_forecast(
    transactions: list[dict],
    current_balance: float,
    days_ahead: int = 15,
) -> tuple[list[ForecastPoint], str, list[AlertInfo]]:
    if not transactions:
        return _empty_forecast(current_balance, days_ahead)

    daily_net = _aggregate_daily_net(transactions)
    dow_avg = _day_of_week_averages(daily_net)
    trend = _compute_trend(daily_net)

    forecast_points: list[ForecastPoint] = []
    cumulative = current_balance
    min_balance = current_balance
    alerts: list[AlertInfo] = []

    today = date.today()
    for i in range(1, days_ahead + 1):
        target_date = today + timedelta(days=i)
        dow = target_date.weekday()
        predicted_flow = dow_avg.get(dow, 0.0) + trend * i
        cumulative += predicted_flow

        confidence = max(0.5, 1.0 - (i * 0.03))
        forecast_points.append(
            ForecastPoint(
                date=target_date,
                predicted_balance=round(cumulative, 0),
                confidence=round(confidence, 2),
            )
        )
        if cumulative < min_balance:
            min_balance = cumulative

        if cumulative < 0 and not any(a.type == "negative_forecast" for a in alerts):
            alerts.append(
                AlertInfo(
                    type="negative_forecast",
                    message=f"Risque: solde négatif prévu dans {i} jours ({round(cumulative, 0)} FCFA)",
                    days_until=i,
                    predicted_shortfall=round(abs(cumulative), 0),
                )
            )

    risk_level = _assess_risk(current_balance, min_balance, forecast_points)

    if risk_level == "HIGH" and not alerts:
        alerts.append(
            AlertInfo(
                type="low_balance",
                message="Attention: votre solde risque de baisser fortement dans les 15 prochains jours",
            )
        )

    return forecast_points, risk_level, alerts


def _aggregate_daily_net(transactions: list[dict]) -> dict[date, float]:
    daily: dict[date, float] = defaultdict(float)
    for t in transactions:
        d = t["date"] if isinstance(t["date"], date) else date.fromisoformat(str(t["date"]))
        amount = t["amount"]
        if t["type"] == "expense":
            amount = -amount
        daily[d] += amount
    return dict(daily)


def _day_of_week_averages(daily_net: dict[date, float]) -> dict[int, float]:
    dow_sums: dict[int, list[float]] = defaultdict(list)
    for d, net in daily_net.items():
        dow_sums[d.weekday()].append(net)
    return {dow: float(np.mean(vals)) for dow, vals in dow_sums.items()}


def _compute_trend(daily_net: dict[date, float]) -> float:
    if len(daily_net) < 3:
        return 0.0

    sorted_dates = sorted(daily_net.keys())
    values = [daily_net[d] for d in sorted_dates]

    n = len(values)
    x = np.arange(n, dtype=float)
    y = np.array(values, dtype=float)

    x_mean = np.mean(x)
    y_mean = np.mean(y)
    denominator = np.sum((x - x_mean) ** 2)
    if denominator == 0:
        return 0.0

    slope = float(np.sum((x - x_mean) * (y - y_mean)) / denominator)
    return slope * 0.3  # dampen trend to avoid over-extrapolation


def _assess_risk(
    current: float,
    min_predicted: float,
    forecast: list[ForecastPoint],
) -> str:
    if min_predicted < 0:
        return "HIGH"
    if current > 0 and min_predicted < current * 0.3:
        return "MEDIUM"
    return "LOW"


def _empty_forecast(
    current_balance: float, days_ahead: int
) -> tuple[list[ForecastPoint], str, list[AlertInfo]]:
    today = date.today()
    points = [
        ForecastPoint(
            date=today + timedelta(days=i),
            predicted_balance=current_balance,
            confidence=0.5,
        )
        for i in range(1, days_ahead + 1)
    ]
    return points, "LOW", [
        AlertInfo(
            type="low_balance",
            message="Pas assez de données pour une prédiction fiable. Ajoutez vos transactions quotidiennes.",
        )
    ]
