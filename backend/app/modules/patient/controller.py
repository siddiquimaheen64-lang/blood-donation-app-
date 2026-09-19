"""
Business logic for the patient module. Routes call these functions;
these functions talk to the database.
"""

from typing import List, Optional

from fastapi import HTTPException, status

from app.models.blood_request import BloodRequest, RequestStatusEnum
from app.models.donor_response import DonorResponse, DonorResponseStatusEnum
from app.models.user import User
from app.modules.patient.schemas import (
    CreateRequest,
    DonorResponseOut,
    MatchedDonorOut,
    RequestOut,
    StatusOut,
)
from app.utils.blood_compatibility import get_compatible_donor_groups


def _to_request_out(req: BloodRequest) -> RequestOut:
    return RequestOut(
        id=str(req.id),
        blood_group=req.blood_group,
        units_needed=req.units_needed,
        units_fulfilled=req.units_fulfilled,
        urgency=req.urgency,
        status=req.status,
        address=req.address,
        patient_name=req.patient_name,
        contact_phone=req.contact_phone,
        compatible_groups=req.compatible_groups,
        created_at=req.created_at,
    )


async def create_blood_request(patient: User, payload: CreateRequest) -> RequestOut:
    compatible_groups = get_compatible_donor_groups(payload.blood_group.value)

    location = {"type": "Point", "coordinates": [payload.lng, payload.lat]}

    new_request = BloodRequest(
        requester_id=patient,
        blood_group=payload.blood_group,
        units_needed=payload.units_needed,
        units_fulfilled=0,
        urgency=payload.urgency,
        status=RequestStatusEnum.PENDING_VERIFICATION,
        location=location,
        address=payload.address,
        patient_name=payload.patient_name,
        contact_phone=payload.contact_phone,
        compatible_groups=compatible_groups,
    )
    await new_request.insert()

    return _to_request_out(new_request)


async def list_my_requests(patient: User) -> List[RequestOut]:
    """FR-08: patient's request history, newest first."""
    requests = (
        await BloodRequest.find(BloodRequest.requester_id.id == patient.id)
        .sort(-BloodRequest.created_at)
        .to_list()
    )
    return [_to_request_out(r) for r in requests]


async def _get_owned_request(patient: User, request_id: str) -> BloodRequest:
    """Fetches a request by id and makes sure it belongs to this patient."""
    req = await BloodRequest.get(request_id)
    if req is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")

    # requester_id is a Link[User]; compare by id
    owner_id = req.requester_id.ref.id if hasattr(req.requester_id, "ref") else req.requester_id.id
    if str(owner_id) != str(patient.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your request")

    return req


async def get_request_status(patient: User, request_id: str) -> StatusOut:
    """FR-09: live progress + populated donor responses."""
    req = await _get_owned_request(patient, request_id)

    responses = await DonorResponse.find(DonorResponse.request_id.id == req.id).to_list()

    percentage = 0.0
    if req.units_needed > 0:
        percentage = round(min(req.units_fulfilled / req.units_needed, 1.0) * 100, 1)

    donor_responses_out = [
        DonorResponseOut(donor_id=str(r.donor_id.ref.id if hasattr(r.donor_id, "ref") else r.donor_id.id), status=r.status.value)
        for r in responses
    ]

    return StatusOut(
        id=str(req.id),
        status=req.status,
        units_needed=req.units_needed,
        units_fulfilled=req.units_fulfilled,
        percentage=percentage,
        donor_responses=donor_responses_out,
    )


async def get_matched_donors(patient: User, request_id: str) -> List[MatchedDonorOut]:
    """FR-09: contact details of donors who ACCEPTED or already DONATED."""
    req = await _get_owned_request(patient, request_id)

    responses = await DonorResponse.find(
        DonorResponse.request_id.id == req.id,
        DonorResponse.status.in_(
            [DonorResponseStatusEnum.ACCEPTED, DonorResponseStatusEnum.DONATED]
        ),
    ).to_list()

    donors_out: List[MatchedDonorOut] = []
    for r in responses:
        donor = await r.donor_id.fetch()  # resolves the Link[User] to a real User document
        if donor is None:
            continue
        donors_out.append(
            MatchedDonorOut(
                name=donor.name,
                phone=donor.phone,
                blood_group=donor.blood_group,
                location=donor.location,
            )
        )

    return donors_out
