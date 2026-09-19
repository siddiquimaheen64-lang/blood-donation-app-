"""
User document. One record per person (patient or donor) who has logged in
through Firebase at least once (created via POST /api/v1/auth/sync).
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

import pymongo
from beanie import Document, Indexed
from pydantic import Field
from pymongo import GEOSPHERE


class RoleEnum(str, Enum):
    PATIENT = "PATIENT"
    DONOR = "DONOR"
    ADMIN = "ADMIN"


class GeoPoint(dict):
    """
    Minimal GeoJSON Point shape, e.g. {"type": "Point", "coordinates": [lng, lat]}.
    NOTE: GeoJSON order is [longitude, latitude], NOT [latitude, longitude].
    """
    pass


class User(Document):
    firebase_uid: Indexed(str, unique=True)  # links this record to the Firebase login
    role: RoleEnum
    name: str
    phone: str
    blood_group: Optional[str] = None  # e.g. "O+" - optional because a patient's family member may not know it
    location: Optional[dict] = None  # GeoJSON Point: {"type": "Point", "coordinates": [lng, lat]}
    fcm_token: Optional[str] = None  # push-notification token, for future donor alerts
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"  # MongoDB collection name
        indexes = [
            [("location", GEOSPHERE)],  # enables geo-queries (find nearby donors later)
        ]
