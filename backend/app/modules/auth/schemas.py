from typing import Optional

from pydantic import BaseModel, Field

from app.models.user import RoleEnum


class SyncRequest(BaseModel):
    idToken: str
    name: str
    phone: str
    blood_group: Optional[str] = None
    role: RoleEnum
    lat: Optional[float] = None
    lng: Optional[float] = None
    fcm_token: Optional[str] = None


class SyncResponse(BaseModel):
    id: str
    firebase_uid: str
    role: RoleEnum
    name: str
    phone: str
    blood_group: Optional[str] = None
    created: bool = Field(description="True if this call created a new user, False if it already existed")
