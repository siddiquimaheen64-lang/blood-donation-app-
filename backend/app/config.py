from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PORT: int = 8000
    MONGO_URI: str = "mongodb://localhost:27017/blood_response"
    MONGO_URL: str = "mongodb://localhost:27017/blood_response"
    MONGODB_URI: str = "mongodb://localhost:27017/blood_response"
    MONGODB_URL: str = "mongodb://localhost:27017/blood_response"
    DB_NAME: str = "blood_response"
    DATABASE_NAME: str = "blood_response"
    FIREBASE_CRED_PATH: str = "./serviceAccountKey.json"
    firebase_uid: str = ""
    FIREBASE_UID: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")

settings = Settings()