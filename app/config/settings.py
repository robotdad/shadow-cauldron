"""
Settings implementation for Shadow Cauldron.

This module handles all configuration through environment variables
and provides validated settings objects.
"""


from pydantic import BaseModel
from pydantic import Field
from pydantic_settings import BaseSettings


class DatabaseConfig(BaseModel):
    """Database configuration model."""

    url: str
    pool_size: int = Field(default=10, ge=1, le=100)
    max_overflow: int = Field(default=20, ge=0, le=100)
    echo: bool = False


class Settings(BaseSettings):
    """
    Main settings class for Shadow Cauldron.

    All settings are loaded from environment variables with SC_ prefix.
    """

    # Application settings
    DEBUG: bool = Field(default=False, description="Enable debug mode")
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, ge=1, le=65535, description="Server port")

    # Security settings
    SECRET_KEY: str = Field(default="dev-secret-key-change-in-production", description="Secret key for JWT tokens")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, ge=1)

    # Database settings
    DATABASE_URL: str = Field(default="sqlite+aiosqlite:///./shadow_cauldron.db", description="Database connection URL")
    DB_POOL_SIZE: int = Field(default=10, ge=1, le=100)
    DB_MAX_OVERFLOW: int = Field(default=20, ge=0, le=100)
    DB_ECHO: bool = Field(default=False, description="Enable SQLAlchemy query logging")

    # CORS settings
    CORS_ORIGINS: list[str] = Field(default=["http://localhost:3000"])

    # AI Provider settings (optional - providers can be configured individually)
    OPENAI_API_KEY: str | None = Field(default=None)
    ANTHROPIC_API_KEY: str | None = Field(default=None)

    class Config:
        env_prefix = "SC_"  # Shadow Cauldron prefix
        case_sensitive = True

    @property
    def database_config(self) -> DatabaseConfig:
        """Get database configuration."""
        return DatabaseConfig(
            url=self.DATABASE_URL,
            pool_size=self.DB_POOL_SIZE,
            max_overflow=self.DB_MAX_OVERFLOW,
            echo=self.DB_ECHO,
        )

    @property
    def sync_database_url(self) -> str:
        """Get synchronous database URL for migrations."""
        return self.DATABASE_URL.replace("sqlite+aiosqlite:", "sqlite:")


# Global settings instance - import this from other bricks
settings = Settings()
