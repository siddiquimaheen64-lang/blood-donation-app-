"""
BloodRequest document - one per blood request created by a patient (FR-02).
"""

from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional

from beanie import Document, Link
from pydantic import Field
from pymongo import GEOSPHERE

from app.models.user import User


class BloodGroupEnum(str, Enum):
    O_NEG = "O-"
    O_POS = "O+"
    A_NEG = "A-"
    A_POS = "A+"
    B_NEG = "B-"
    B_POS = "B+"
    AB_NEG = "AB-"
    AB_POS = "AB+"


class UrgencyEnum(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RequestStatusEnum(str, Enum):
    PENDING_VERIFICATION = "PENDING_VERIFICATION"  # just created, waiting for admin/hospital to verify
    OPEN = "OPEN"                                   # verified, visible to donors
    MATCHED = "MATCHED"                             # at least one donor accepted
    PARTIALLY_FULFILLED = "PARTIALLY_FULFILLED"     # some units donated, not all
    FULFILLED = "FULFILLED"                         # units_fulfilled >= units_needed
    CLOSED = "CLOSED"                               # manually closed (e.g. patient no longer needs it)
    REJECTED = "REJECTED"                           # failed verification


class BloodRequest(Document):
    requester_id: Link[User]  # the patient (User) who created this request

    blood_group: BloodGroupEnum
    units_needed: int
    units_fulfilled: int = 0

    urgency: UrgencyEnum

    status: RequestStatusEnum = RequestStatusEnum.PENDING_VERIFICATION

    # location as GeoJSON Point: {"type": "Point", "coordinates": [lng, lat]}
    location: dict
    address: str

    patient_name: str
    contact_phone: str

    # auto-calculated from COMPATIBILITY_MAP at creation time (FR-02)
    compatible_groups: List[str] = Field(default_factory=list)

    verified_by: Optional[str] = None  # admin/hospital user id who verified this request

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "blood_requests"
        indexes = [
            [("location", GEOSPHERE)],
        ]
