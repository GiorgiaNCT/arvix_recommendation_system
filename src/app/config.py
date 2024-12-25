from pydantic import BaseSettings
from typing import List
from functools import lru_cache

class Settings(BaseSettings):
    # App configuration
    APP_TITLE: str = "arXiv Paper Search API"
    APP_DESCRIPTION: str = "API to search for academic papers on arXiv"
    APP_VERSION: str = "1.0.0"
    
    # API Configuration
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    
    # CORS Settings
    ALLOWED_ORIGINS: List[str] = ["*"]
    ALLOWED_METHODS: List[str] = ["*"]
    ALLOWED_HEADERS: List[str] = ["*"]
    ALLOW_CREDENTIALS: bool = True
    
    # ArXiv API Settings
    ARXIV_BASE_URL: str = "http://export.arxiv.org/api/query"
    ARXIV_MAX_RESULTS: int = 100
    ARXIV_DEFAULT_SORT: str = "lastUpdatedDate"
    
    # Cache Settings
    CACHE_TTL: int = 3600  # 1 hour in seconds
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """
    Creates cached instance of settings.
    Use this instead of creating a new Settings instance each time.
    """
    return Settings()