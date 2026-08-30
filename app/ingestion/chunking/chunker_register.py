from __future__ import annotations

from app.ingestion.chunking.interfaces.base_chunker import BaseChunker

class ChunkerRegistry:
    """
        Registry for chunking registry
    """

    _registry: dict[str, type[BaseChunker]] = {}

    @classmethod
    def register(cls, chunker: type[BaseChunker]) -> type[BaseChunker]:

        name  = chunker.name().lower()

        print("chunker-------> ")

        if name in cls._registry:
            raise ValueError(f"chunker '{name}' is already registered.")
        
        cls._registry[name] = chunker

        return chunker
    

    @classmethod
    def get(cls, strategy: str) -> type[BaseChunker]:

        chunker = cls._registry.get(strategy.lower())

        if chunker is None:
            supported = ", ".join(sorted(cls._registry.keys()))

            raise ValueError(
                f"Unknown chunking strategy '{strategy} ."
                f"supported strategies: {supported}."
            )
        
        return chunker
