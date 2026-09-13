from __future__ import annotations

from app.retrieval.metadata_filtering.interfaces.base_metadata_filter import BaseMetadataFilter

class MetadataFilterRegistry:

    _registry: dict[str, type[BaseMetadataFilter]] = {}

    @classmethod
    def register(cls, provider: type[BaseMetadataFilter]) -> type[BaseMetadataFilter]:

        """
            register metadata filter provider
        """

        name = provider.name().lower()

        if name in cls._registry:
            raise ValueError(
                f"Query Rewriter '{name}' is already registered."
            )
        
        cls._registry[name] = provider

        return provider
    

    @classmethod
    def get(cls, provider_name: str) -> type[BaseMetadataFilter]:

        provider = cls._registry.get(provider_name.lower())

        if provider is None:
            supported = ", ".join(
                sorted(cls._registry.keys())
            )

            raise ValueError(
                f"Unknown query rewriter: '{provider_name}'. "
                f"Supported providers: {supported}"
            )
        
        return provider