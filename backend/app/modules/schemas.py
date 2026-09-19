from pydantic import BaseModel

class SyncRequest(BaseModel):
    id_token: str

class SyncResponse(BaseModel):
    uid: str
    message: str = "ok"