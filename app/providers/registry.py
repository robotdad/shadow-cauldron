"""
Provider registry for managing AI service providers.

Central registry that handles provider discovery, instantiation, and management.
"""


import structlog

from .base import BaseProvider
from .base import ProviderConfig

logger = structlog.get_logger(__name__)


class ProviderRegistry:
    """
    Central registry for AI providers.

    Manages registration, instantiation, and lifecycle of AI providers.
    Supports plugin-style architecture where providers can be added dynamically.
    """

    def __init__(self):
        self._provider_classes: dict[str, type[BaseProvider]] = {}
        self._provider_instances: dict[str, BaseProvider] = {}

    def register_provider(self, provider_class: type[BaseProvider]) -> None:
        """
        Register a provider class.

        Args:
            provider_class: Provider class that implements BaseProvider
        """
        # Get provider name from class name or config
        provider_name = getattr(provider_class, "PROVIDER_NAME", provider_class.__name__.lower())

        self._provider_classes[provider_name] = provider_class
        logger.info("Provider registered", provider=provider_name)

    def create_provider(self, name: str, config: ProviderConfig) -> BaseProvider:
        """
        Create a provider instance.

        Args:
            name: Provider name
            config: Provider configuration

        Returns:
            Configured provider instance

        Raises:
            KeyError: If provider is not registered
        """
        if name not in self._provider_classes:
            available = list(self._provider_classes.keys())
            raise KeyError(f"Provider '{name}' not found. Available: {available}")

        provider_class = self._provider_classes[name]
        instance = provider_class(config)

        # Store instance for reuse
        self._provider_instances[name] = instance

        logger.info("Provider created", provider=name, enabled=config.enabled)
        return instance

    def get_provider(self, name: str) -> BaseProvider | None:
        """
        Get a provider instance by name.

        Args:
            name: Provider name

        Returns:
            Provider instance if found and enabled, None otherwise
        """
        instance = self._provider_instances.get(name)
        if instance and instance.is_enabled():
            return instance
        return None

    def list_providers(self) -> list[str]:
        """List all registered provider names."""
        return list(self._provider_classes.keys())

    def list_enabled_providers(self) -> list[str]:
        """List names of enabled provider instances."""
        enabled = []
        for name, instance in self._provider_instances.items():
            if instance.is_enabled():
                enabled.append(name)
        return enabled


# Global registry instance
_registry = ProviderRegistry()


def get_registry() -> ProviderRegistry:
    """Get the global provider registry."""
    return _registry


def get_provider(name: str) -> BaseProvider | None:
    """Get a provider instance by name from the global registry."""
    return _registry.get_provider(name)


def list_providers() -> list[str]:
    """List all registered providers from the global registry."""
    return _registry.list_providers()
