"""
FastAPI dependencies for authentication and role-based authorization.

Usage in a route:

    @router.post("/requests")
    async def create_request(user: User = Depends(authenticate)):
        ...

    @router.get("/admin-only")
    async def admin_stuff(user: User = Depends(authorize(["ADMIN"]))):
        ...
"""

from firebase_admin import auth as firebase_auth
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.models.user import User

bearer_scheme = HTTPBearer()


async def authenticate(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> User:
    """
    Reads the "Authorization: Bearer <idToken>" header, verifies it with
    Firebase, then looks up the matching User document in MongoDB.
    Raises 401 if the token is invalid or the user hasn't synced yet.
    """
    token = credentials.credentials

    try:
        decoded_token = firebase_auth.verify_id_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired Firebase token",
        )

    firebase_uid = decoded_token["uid"]

    user = await User.find_one(User.firebase_uid == firebase_uid)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found. Call /api/v1/auth/sync first.",
        )

    return user


def authorize(allowed_roles: list[str]):
    """
    Returns a dependency that first authenticates, then checks the user's
    role is in allowed_roles. e.g. Depends(authorize(["PATIENT"]))
    """

    async def _check_role(user: User = Depends(authenticate)) -> User:
        if user.role.value not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires one of roles: {allowed_roles}",
            )
        return user

    return _check_role
