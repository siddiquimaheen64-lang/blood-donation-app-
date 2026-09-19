"""
Patient-facing endpoints (Option 1 in the PRD: Patients / Patient Families).

All routes require a logged-in PATIENT (Depends(authorize(["PATIENT"]))).
"""

from typing import List

from fastapi import APIRouter, Depends

from app.middlewares.auth import authorize
from app.models.user import User
from app.modules.patient import controller
from app.modules.patient.schemas import (
    CreateRequest,
    MatchedDonorOut,
    RequestOut,
    StatusOut,
)

router = APIRouter(prefix="/api/v1/patient", tags=["patient"])

patient_only = authorize(["PATIENT"])


@router.post("/requests", response_model=RequestOut)
async def create_request(payload: CreateRequest, patient: User = Depends(patient_only)):
    """FR-02: create a new blood request."""
    return await controller.create_blood_request(patient, payload)


@router.get("/requests", response_model=List[RequestOut])
async def my_requests(patient: User = Depends(patient_only)):
    """FR-08: view history of previous requests."""
    return await controller.list_my_requests(patient)


@router.get("/requests/{request_id}/status", response_model=StatusOut)
async def request_status(request_id: str, patient: User = Depends(patient_only)):
    """FR-09: live progress (units fulfilled / needed, percentage, donor responses)."""
    return await controller.get_request_status(patient, request_id)


@router.get("/requests/{request_id}/donors", response_model=List[MatchedDonorOut])
async def matched_donors(request_id: str, patient: User = Depends(patient_only)):
    """FR-09: contact info of ACCEPTED/DONATED donors only."""
    return await controller.get_matched_donors(patient, request_id)
