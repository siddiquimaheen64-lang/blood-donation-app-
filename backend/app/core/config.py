from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PORT: int = 8000
    MONGO_URL: str
    DB_NAME: str
    JWT_SECRET: str
    FIREBASE_CRED_PATH: str = "./serviceAccountKey.json"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")

settings = Settings()