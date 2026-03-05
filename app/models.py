from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    transaction_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    transaction_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    country: Mapped[str] = mapped_column(String(2), nullable=False, index=True)
    risk_level: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    risk_reason: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), default=datetime.now, nullable=False
    )
