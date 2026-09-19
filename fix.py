import pathlib, shutil
app = pathlib.Path("app")
models = app / "models"

# 1. Fix request.py
if (models / "blood_request.py").exists() and not (models / "request.py").exists():
    shutil.copy(models / "blood_request.py", models / "request.py")
    print("fixed request.py")

# 2. Fix response.py - create if missing
if not (models / "response.py").exists():
    # try to copy blood_response.py if exists
    if (models / "blood_response.py").exists():
        shutil.copy(models / "blood_response.py", models / "response.py")
    else:
        # create a stub file that will work for now
        (models / "response.py").write_text("""
from pydantic import BaseModel
from typing import Optional

class DonorResponse(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    blood_group: Optional[str] = None
    phone: Optional[str] = None
    message: str = "ok"

class BloodResponse(BaseModel):
    message: str = "ok"
""")
    print("fixed response.py")

# 3. Fix any other missing aliases
for real in models.glob("blood_*.py"):
    short = models / (real.name.replace("blood_", ""))
    if not short.exists():
        shutil.copy(real, short)
        print(f"fixed {short.name}")

print("FIX DONE - now run uvicorn")