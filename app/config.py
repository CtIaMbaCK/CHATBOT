import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "MyApp"
    # Database
    DATABASE_URL: str
    PGVECTOR_DIM: int = 1024
    DATABASE_URL_ASYNC: str 

    # Embedding model
    EMBED_MODEL_NAME: str
    MODEL_ID: str = "BAAI/bge-m3"

    # Gemini
    GEMINI_API_KEY: str
    GEMINI_MODEL: str

    #mail
    SMTP_EMAIL: str
    SMTP_PASSWORD: str
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    FRONTEND_URL: str = "http://localhost:3000"
    BACKEND_URL: str = "http://127.0.0.1:8000"
    
    google_client_id: str
    google_client_secret: str
    api_backend_domain: str
    nextauth_url: str
    nextauth_secret: str

    # JWT
    # JWT_SECRET_KEY: str
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "super-secret")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    # Paths
    # DATA_PATH: str = "app/data/"
    DATA_PATH_ADMISSIONS: str = "data/admissions_20250623.json"
    DATA_PATH_STUDENTS: str = "data/students_20250623.json"
    PDF_DIR: str = "data/static/pdfs/"
    STATIC_PDFS_PATH: str = "data/static/pdfs/"
    LOG_PATH: str = "logs/app.log"

    # Environment
    ENV: str = "development"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()