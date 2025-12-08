from typing import List
from pydantic import BaseModel

class ClinicalRecordBase(BaseModel):
    subject_id: str
    age: int
    gender: str
    treatment_arm: str
    site: str
    visit_date: str

class ClinicalRecordRead(ClinicalRecordBase):
    id: int

    class Config:
        from_attributes = True

class SummaryItem(BaseModel):
    label: str
    count: int

class DemographicsSummary(BaseModel):
    by_gender: List[SummaryItem]
    by_treatment_arm: List[SummaryItem]
