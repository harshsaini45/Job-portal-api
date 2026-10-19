from pydantic_settings import BaseSettings
from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta, timezone


class Settings(BaseSettings):
    APP_NAME: str = "Job Portal API"
    DATABASE_URL: str = "postgresql+psycopg://postgres:1234@localhost:5432/job_portal_db"
    


    class Config:
        env_file = ".env"

password_hash = PasswordHash.recommended()

SECRET_KEY = "job_portal_secret_key_2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    ) 
    to_encode.update({"exp": expire})
    
    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token



settings = Settings()