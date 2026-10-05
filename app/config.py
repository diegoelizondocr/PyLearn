from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    oracle_user: str = "MyTestDB"
    oracle_password: str = "MyTestDB123"
    oracle_dsn: str = "localhost:1521/FREEPDB1"

    resend_api_key: str = ""
    resend_from_email: str = "onboarding@resend.dev"

    app_title: str = "MyTestDB API"
    app_description: str = "API de aprendizaje con Oracle + FastAPI"
    app_version: str = "1.0.0"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()