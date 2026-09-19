from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.blood_request import BloodGroupEnum, RequestStatusEnum, UrgencyEnum


class CreateRequest(BaseModel):
    blood_group: BloodGroupEnum
    units_needed: int = Field(gt=0, description="Must be at least 1")
    lat: float
    lng: float
    address: str
    urgency: UrgencyEnum
    patient_name: str
    contact_phone: str


class RequestOut(BaseModel):
    id: str
    blood_group: BloodGroupEnum
    units_needed: int
    units_fulfilled: int
    urgency: UrgencyEnum
    status: RequestStatusEnum
    address: str
    patient_name: str
    contact_phone: str
    compatible_groups: List[str]
    created_at: datetime


class DonorResponseOut(BaseModel):
    donor_id: str
    status: str


class StatusOut(BaseModel):
    id: str
    status: RequestStatusEnum
    units_needed: int
    units_fulfilled: int
    percentage: float
    donor_responses: List[DonorResponseOut]


class MatchedDonorOut(BaseModel):
    name: str
    phone: str
    blood_group: Optional[str] = None
    location: Optional[dict] = None
