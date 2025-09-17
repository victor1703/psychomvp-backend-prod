from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./psychomvp.db"
    SECRET_KEY: str = "changeme"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30
    ALLOWED_ORIGINS: str = ""  # CSV
    CORS_ALLOW_ALL: bool = False
    PROJECT_NAME: str = "PsicoMVP API"
    ENV: str = "prod"  # prod | local
    AUTO_CREATE_TABLES: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def allowed_origins_list(self) -> List[str]:
        if self.CORS_ALLOW_ALL:
            return ["*"]
        if not self.ALLOWED_ORIGINS:
            return []
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",") if o.strip()]

settings = Settings()
