"""
Providers Brick

PUBLIC CONTRACT:
- ProviderRegistry: Central registry for AI providers
- BaseProvider: Abstract base class for all providers
- get_provider(name): Factory function to get provider instances
- list_providers(): List all available providers

RESPONSIBILITIES:
- AI provider abstraction and plugin system
- Provider registration and discovery
- Common interface for different AI services
- Provider-specific configuration and authentication
"""

from .base import BaseProvider
from .registry import ProviderRegistry
from .registry import get_provider
from .registry import list_providers

__all__ = ["ProviderRegistry", "BaseProvider", "get_provider", "list_providers"]
