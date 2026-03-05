from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import RiskAssessmentRequest, RiskAssessmentResponse
from app.services.risk_service import assess_transaction

router = APIRouter()

@router.post("/assess-risk", response_model=RiskAssessmentResponse, status_code=status.HTTP_201_CREATED)
def assess_risk(
    payload: RiskAssessmentRequest,
    db: Session = Depends(get_db),
) -> RiskAssessmentResponse:
    return assess_transaction(payload, db)
