from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str = "CHANGE_ME"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    DATABASE_URL: str = "sqlite:///./app.db"

    # Pydantic v2 config style
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",  # ignore any unexpected env vars
    )

settings = Settings()
