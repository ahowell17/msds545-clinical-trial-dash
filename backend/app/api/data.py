from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.security import get_current_active_user
from app.db.session import get_db
from app.db import models
from app.schemas.data import DemographicsSummary, SummaryItem

router = APIRouter(prefix="/data", tags=["data"])

@router.get("/demographics", response_model=DemographicsSummary)
def get_demographics_summary(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    gender_rows = (
        db.query(models.ClinicalRecord.gender, func.count(models.ClinicalRecord.id))
        .group_by(models.ClinicalRecord.gender)
        .all()
    )
    by_gender: List[SummaryItem] = [
        SummaryItem(label=g or "Unknown", count=c) for g, c in gender_rows
    ]

    arm_rows = (
        db.query(models.ClinicalRecord.treatment_arm, func.count(models.ClinicalRecord.id))
        .group_by(models.ClinicalRecord.treatment_arm)
        .all()
    )
    by_treatment_arm: List[SummaryItem] = [
        SummaryItem(label=a or "Unknown", count=c) for a, c in arm_rows
    ]

    return DemographicsSummary(by_gender=by_gender, by_treatment_arm=by_treatment_arm)
