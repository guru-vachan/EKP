from __future__ import annotations

from app.embeddings.interfaces.base_embedding import BaseEmbedding
from app.core.exceptions import UnsupportedEmbeddingProvider

class EmbeddingRegistry:
    """
        Registry for embedding providers.
    """

    _registry: dict[str, type[BaseEmbedding]] = {}


    @classmethod
    def register(cls, provider: type[BaseEmbedding]) -> type[BaseEmbedding]:

        name = provider.name().lower()

        if name in cls._registry:
            raise ValueError(
                f"Embedding provider '{name}' is already registered."
            )
        
        cls._registry[name] = provider

        return provider
    

    @classmethod
    def get(cls, provider_name: str) -> type[BaseEmbedding]:

        provider = cls._registry.get(provider_name.lower())

        if provider is None:
            supported = ", ".join(
                sorted(cls._registry.keys())
            )

            raise UnsupportedEmbeddingProvider(
                f"Unknown embedding provider: '{provider_name}'. "
                f"Supported providers: {supported}"
            )
        
        return provider
