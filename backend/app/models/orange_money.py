from datetime import datetime

from sqlalchemy import String, DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class OrangeMoneyAccount(Base):
    __tablename__ = "orange_money_accounts"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), primary_key=True
    )
    encrypted_token: Mapped[str | None] = mapped_column(String(512))
    last_sync: Mapped[datetime | None] = mapped_column(DateTime)
    balance: Mapped[float] = mapped_column(Float, default=0.0)

    user: Mapped["User"] = relationship(back_populates="orange_money_account")
