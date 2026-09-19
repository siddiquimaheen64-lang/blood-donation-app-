import certifi
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.models.user import User
from app.models.blood_request import BloodRequest
from app.models.donor_response import DonorResponse
from app.modules.auth.routes import router as auth_router
from app.modules.patient.routes import router as patient_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    client = AsyncIOMotorClient(
        settings.MONGO_URL,
        tlsCAFile=certifi.where()
        # Remove tlsAllowInvalidCertificates=True for production
    )
    await init_beanie(
        database=client[settings.DB_NAME],
        document_models=[User, BloodRequest, DonorResponse]
    )
    print("Connected to MongoDB")
    yield
    # --- Shutdown ---
    client.close()

app = FastAPI(
    title="Al-Khidmat Blood Response API",
    version="1.0.0",
    lifespan=lifespan
)

# FIXED CORS - ["*"] + credentials=True crashes browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],
    allow_credentials=False,  # Must be False if origins is ["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(patient_router, prefix="/api/patient", tags=["Patient"])

@app.get("/")
async def root():
    return {"message": "Al-Khidmat Blood Response API is running"}