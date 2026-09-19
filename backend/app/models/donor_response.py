"""
DonorResponse document - tracks how each notified donor responded to a
specific blood request. One row per (request, donor) pair.
"""

from datetime import datetime, timezone
from enum import Enum

from beanie import Document, Link
from pydantic import Field
from pymongo import ASCENDING, IndexModel

from app.models.blood_request import BloodRequest
from app.models.user import User


class DonorResponseStatusEnum(str, Enum):
    NOTIFIED = "NOTIFIED"
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"
    DONATED = "DONATED"

class DonorResponse(Document):
    request_id: Link[BloodRequest]
    donor_id: Link[User]

    status: DonorResponseStatusEnum = DonorResponseStatusEnum.NOTIFIED

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "donor_responses"
        indexes = [
            # a donor can only have ONE response per request (no duplicate notifications)
            IndexModel(
                [("request_id", ASCENDING), ("donor_id", ASCENDING)],
                unique=True,
                name="unique_request_donor",
            ),
        ]
