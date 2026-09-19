from pydantic import BaseModel
from typing import Optional

class DonorResponse(BaseModel):
    id: Optional[str] = None
    message: str = "ok"

class BloodResponse(BaseModel):
    message: str = "ok"