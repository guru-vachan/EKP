from __future__ import annotations

from app.retrieval.query_rewriting.interfaces.base_query_rewriter import BaseQueryRewriter

class QueryRewriterRegistry:

    _registry: dict[str, type[BaseQueryRewriter]] = {}


    @classmethod
    def register(cls, provider: type[BaseQueryRewriter]) -> type[BaseQueryRewriter]:

        name = provider.name().lower()

        if name in cls._registry:
            raise ValueError(
                f"Query Rewriter '{name}' is already registered."
            )
        
        cls._registry[name] = provider

        return provider
    

    @classmethod
    def get(cls, provider_name: str) -> type[BaseQueryRewriter]:

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
     
     

