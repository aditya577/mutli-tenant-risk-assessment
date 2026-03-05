from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import RiskAssessment
from app.schemas import RiskAssessmentRequest, RiskAssessmentResponse, RiskLevel

ALLOWED_COUNTRIES = {"CA", "US", "UK"}
HIGH_RISK_THRESHOLD = Decimal("10000")


def determine_risk(transaction_amount: Decimal, country: str) -> tuple[RiskLevel, str]:
    if transaction_amount > HIGH_RISK_THRESHOLD:
        return RiskLevel.HIGH, "transaction_amount is greater than 10000"

    if country not in ALLOWED_COUNTRIES:
        return RiskLevel.MEDIUM, f"country '{country}' is outside the allowed list"

    return RiskLevel.LOW, "transaction meets baseline checks"


def assess_transaction(payload: RiskAssessmentRequest, db: Session) -> RiskAssessmentResponse:
    risk_level, reason = determine_risk(payload.transaction_amount, payload.country)

    assessment = RiskAssessment(
        transaction_id=payload.transaction_id,
        transaction_amount=payload.transaction_amount,
        country=payload.country,
        risk_level=risk_level.value,
        risk_reason=reason,
    )

    try:
        db.add(assessment)
        db.commit()
        db.refresh(assessment)
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to persist risk assessment.",
        ) from exc

    return RiskAssessmentResponse(
        assessment_id=assessment.id,
        transaction_id=assessment.transaction_id,
        transaction_amount=assessment.transaction_amount,
        country=assessment.country,
        risk_level=RiskLevel(assessment.risk_level),
        risk_reason=assessment.risk_reason,
        created_at=assessment.created_at,
    )
