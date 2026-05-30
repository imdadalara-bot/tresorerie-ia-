import uuid
from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    email: Mapped[str | None] = mapped_column(String(255), unique=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(20), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    hashed_password: Mapped[str] = mapped_column(String(255))
    sector: Mapped[str] = mapped_column(String(20), default="commercant")
    currency: Mapped[str] = mapped_column(String(3), default="XOF")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    transactions: Mapped[list["Transaction"]] = relationship(back_populates="user")
    orange_money_account: Mapped["OrangeMoneyAccount | None"] = relationship(
        back_populates="user", uselist=False
    )
    forecasts: Mapped[list["Forecast"]] = relationship(back_populates="user")
    alerts: Mapped[list["Alert"]] = relationship(back_populates="user")
