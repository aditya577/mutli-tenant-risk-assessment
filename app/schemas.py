from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class RiskLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIM"
    LOW = "LOW"


class RiskAssessmentRequest(BaseModel):
    transaction_id: str = Field(..., min_length=1, max_length=64)
    transaction_amount: Decimal = Field(..., gt=0, max_digits=12, decimal_places=2)
    country: str = Field(..., min_length=2, max_length=2)

    @field_validator("transaction_id")
    @classmethod
    def clean_transaction_id(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("transaction_id should not be blank.")
        return cleaned

    @field_validator("country")
    @classmethod
    def validate_country_code(cls, value: str) -> str:
        normalized = value.strip().upper()
        if len(normalized) != 2 or not normalized.isalpha():
            raise ValueError("country code must be a 2 letter ISO code.")
        return normalized


class RiskAssessmentResponse(BaseModel):
    assessment_id: int
    transaction_id: str
    transaction_amount: Decimal
    country: str
    risk_level: RiskLevel
    risk_reason: str
    created_at: datetime
