# data/config/settings.py
"""
Application settings and configuration
Based on: TodoApp environment variables and configuration

Note: This in the future has some items that needs to be environment variables
"""

import os
from typing import Optional
from functools import lru_cache


class Settings:
    """
    Application settings loaded from environment variables
    """
    
    def __init__(self):
        # Database settings
        self.DATABASE_URL: str = os.getenv(
            "DATABASE_URL",
            "sqlite:///./todosapp.db"
        )
        
        # JWT settings
        self.SECRET_KEY: str = os.getenv(
            "SECRET_KEY",
            "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
        )
        self.ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "20")
        )
        
        # Application settings
        self.APP_NAME: str = os.getenv("APP_NAME", "TodoApp")
        self.DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance
    Using lru_cache to avoid reading environment variables multiple times
    """
    return Settings()