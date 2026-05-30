"""PDF export for bank/microfinance sharing."""

import io
from datetime import date, timedelta

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from app.database import get_db
from app.models.user import User
from app.models.transaction import Transaction
from app.services.auth import get_current_user

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/pdf")
def export_pdf(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    since = date.today() - timedelta(days=days)
    txns = (
        db.query(Transaction)
        .filter(
            Transaction.user_id == current_user.id,
            Transaction.date >= since,
        )
        .order_by(Transaction.date)
        .all()
    )

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(f"Trésorier IA — Rapport financier", styles["Title"]))
    elements.append(Paragraph(f"Utilisateur: {current_user.name}", styles["Normal"]))
    elements.append(Paragraph(f"Secteur: {current_user.sector}", styles["Normal"]))
    elements.append(
        Paragraph(
            f"Période: {since.isoformat()} → {date.today().isoformat()}",
            styles["Normal"],
        )
    )
    elements.append(Spacer(1, 0.5 * cm))

    total_income = sum(t.amount for t in txns if t.type == "income")
    total_expense = sum(t.amount for t in txns if t.type == "expense")
    net = total_income - total_expense

    summary_data = [
        ["Entrées totales", f"{total_income:,.0f} {current_user.currency}"],
        ["Sorties totales", f"{total_expense:,.0f} {current_user.currency}"],
        ["Solde net", f"{net:,.0f} {current_user.currency}"],
    ]
    summary_table = Table(summary_data, colWidths=[8 * cm, 6 * cm])
    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTSIZE", (0, 0), (-1, -1), 11),
            ]
        )
    )
    elements.append(summary_table)
    elements.append(Spacer(1, 0.5 * cm))

    elements.append(Paragraph("Détail des transactions", styles["Heading2"]))
    table_data = [["Date", "Type", "Montant", "Source", "Note"]]
    for t in txns:
        table_data.append([
            t.date.isoformat(),
            "Entrée" if t.type == "income" else "Sortie",
            f"{t.amount:,.0f}",
            t.source,
            t.note or "",
        ])

    if len(table_data) > 1:
        detail_table = Table(table_data, colWidths=[3 * cm, 2.5 * cm, 3 * cm, 3 * cm, 4 * cm])
        detail_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563eb")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f4ff")]),
                ]
            )
        )
        elements.append(detail_table)
    else:
        elements.append(Paragraph("Aucune transaction sur cette période.", styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=tresorier_rapport_{date.today()}.pdf"},
    )
