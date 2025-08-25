"""
Configuration Brick

PUBLIC CONTRACT:
- settings: Global settings instance
- DatabaseConfig: Database configuration model
- Settings: Main settings class

RESPONSIBILITIES:
- Environment variable management
- Configuration validation
- Database connection strings
- API keys and secrets management
"""

from .settings import DatabaseConfig
from .settings import Settings
from .settings import settings

__all__ = ["settings", "Settings", "DatabaseConfig"]
