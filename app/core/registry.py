from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")


class Registry(Generic[T]):
    """
        Generic registry for provider implementation.
    """

    def __init__(self) -> None:
        self._registry: dict[str, type[T]] = {}
    


    def register(self, provider: type[T]) -> type[T]:
        """
            Register a provider.
        """

        name = provider.name().lower()

        if name in self._registry:
            raise ValueError(
                f"'{name}' is already registered."
            )
        
        self._registry[name] = provider

        return provider
    

    def get(cls, provider_name: str) -> type[T]:

        provider = cls._registry.get(provider_name.lower())

        if provider is None:
            supported = ", ".join(
                sorted(cls._registry.keys())
            )

            raise ValueError(
                f"Unknown provider: '{provider_name}'. "
                f"Supported providers: {supported}"
            )
        
        return provider
    

    def registered_providers(self, ) -> tuple[str, ...]:

        return tuple(
            sorted(self._registry.keys())
        )