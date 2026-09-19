from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.get("/test")
def test_auth():
    return {"status": "auth module works"}

@router.post("/sync")
def sync_user():
    return {"message": "user synced", "uid": "test123"}

@router.get("/me")
def get_me():
    return {"user": "demo"}