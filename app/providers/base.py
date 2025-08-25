"""
Base provider interface for AI services.

Defines the common contract that all AI providers must implement.
"""

from abc import ABC
from abc import abstractmethod
from typing import Any

from pydantic import BaseModel


class ProviderConfig(BaseModel):
    """Base configuration for AI providers."""

    name: str
    enabled: bool = True
    api_key: str | None = None
    base_url: str | None = None
    timeout: int = 30
    max_retries: int = 3


class CompletionRequest(BaseModel):
    """Standard request format for text completions."""

    prompt: str
    model: str
    max_tokens: int | None = None
    temperature: float | None = None
    system_prompt: str | None = None


class CompletionResponse(BaseModel):
    """Standard response format for text completions."""

    text: str
    model: str
    provider: str
    usage: dict[str, Any] | None = None
    metadata: dict[str, Any] | None = None


class BaseProvider(ABC):
    """
    Abstract base class for all AI providers.

    This defines the common interface that all providers must implement,
    enabling the plugin system to work with different AI services uniformly.
    """

    def __init__(self, config: ProviderConfig):
        self.config = config
        self.name = config.name

    @abstractmethod
    async def complete(self, request: CompletionRequest) -> CompletionResponse:
        """
        Generate a text completion.

        Args:
            request: Completion request with prompt and parameters

        Returns:
            Completion response with generated text and metadata
        """
        pass

    @abstractmethod
    async def list_models(self) -> list[str]:
        """
        List available models for this provider.

        Returns:
            List of model names/identifiers
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Check if the provider is healthy and accessible.

        Returns:
            True if provider is healthy, False otherwise
        """
        pass

    def is_enabled(self) -> bool:
        """Check if this provider is enabled."""
        return self.config.enabled
