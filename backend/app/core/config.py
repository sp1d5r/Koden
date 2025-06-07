import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Koden Backend"
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/dev_db"
    )
    
    # Firebase
    FIREBASE_PROJECT_ID: str = os.getenv("FIREBASE_PROJECT_ID", "")
    FIREBASE_PRIVATE_KEY_ID: str = os.getenv("FIREBASE_PRIVATE_KEY_ID", "")
    FIREBASE_PRIVATE_KEY: str = os.getenv("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n")
    FIREBASE_CLIENT_EMAIL: str = os.getenv("FIREBASE_CLIENT_EMAIL", "")
    FIREBASE_CLIENT_ID: str = os.getenv("FIREBASE_CLIENT_ID", "")
    FIREBASE_AUTH_URI: str = os.getenv("FIREBASE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth")
    FIREBASE_TOKEN_URI: str = os.getenv("FIREBASE_TOKEN_URI", "https://oauth2.googleapis.com/token")
    FIREBASE_AUTH_PROVIDER_X509_CERT_URL: str = os.getenv(
        "FIREBASE_AUTH_PROVIDER_X509_CERT_URL",
        "https://www.googleapis.com/oauth2/v1/certs"
    )
    FIREBASE_CLIENT_X509_CERT_URL: str = os.getenv("FIREBASE_CLIENT_X509_CERT_URL", "")

    class Config:
        case_sensitive = True

settings = Settings() 