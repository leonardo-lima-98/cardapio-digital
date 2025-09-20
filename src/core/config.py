## 1. Configurações (src/core/config.py)

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    
    # App Settings
    DEBUG: bool = False
    APP_NAME: str = "Digital Menu System"
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = "sqlite:///./digital_menu.db"
    
    # JWT Settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    @property
    def database_url(self) -> str:
        if self.DEBUG:
            return "sqlite:///./digital_menu.db"
        return self.DATABASE_URL

settings = Settings()