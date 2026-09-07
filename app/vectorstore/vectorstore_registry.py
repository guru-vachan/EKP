from __future__ import annotations

from app.vectorstore.interface.base_vectorstore import BaseVectorStore
from app.core.exceptions import UnsupportedVectorStoreProvider

class VectorStoreRegistry:

    _registry: dict[str, type[BaseVectorStore]] = {}


    @classmethod
    def register(cls, provider: type[BaseVectorStore]) -> type[BaseVectorStore]:

        name = provider.name().lower()

        if name in cls._registry:
            raise ValueError(
                f"vectorstore provider '{name}' is already registered."
            )
        
        cls._registry[name] = provider

        return provider
    

    @classmethod
    def get(cls, provider_name: str) -> type[BaseVectorStore]:

        provider = cls._registry.get(provider_name.lower())

        if provider is None:
            raise UnsupportedVectorStoreProvider(
                f"Unknown embedding provider: '{provider_name}'. "
            )
        
        return provider
    
    
    @classmethod
    def registered_providers(cls, ) -> tuple[str, ...]:

        return tuple(
            sorted(cls._registry.keys())
        )