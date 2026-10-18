from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Job Portal API"
    DATABASE_URL: str = "postgresql+psycopg://postgres:password@localhost:5432/job_portal_db"

    class Config:
        env_file = ".env"


settings = Settings()