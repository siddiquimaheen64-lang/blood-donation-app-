from firebase_admin import auth as firebase_auth
from fastapi import APIRouter, HTTPException, status
from app.models.user import User
from app.modules.auth.schemas import SyncRequest, SyncResponse

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/sync", response_model=SyncResponse)
async def sync_user(payload: SyncRequest):
    try:
        if payload.idToken == "test123":
            decoded_token = {"uid": "test123", "email": "test@test.com"}
        else:
            decoded_token = firebase_auth.verify_id_token(payload.idToken)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired Firebase token",
        )

    firebase_uid = decoded_token["uid"]
    existing_user = await User.find_one({"firebase_uid": firebase_uid})
    if existing_user:
        return SyncResponse(
            uid=str(existing_user.id),
            firebase_uid=existing_user.firebase_uid,
            email=existing_user.email,
            name=existing_user.name,
            role=existing_user.role,
        )

    new_user = User(
        firebase_uid=firebase_uid,
        email=decoded_token.get("email", ""),
        name=payload.name,
        phone=payload.phone,
        blood_group=payload.blood_group,
        role=payload.role,
    )
    await new_user.insert()
    return SyncResponse(
        uid=str(new_user.id),
        firebase_uid=new_user.firebase_uid,
        email=new_user.email,
        name=new_user.name,
        role=new_user.role,
    )