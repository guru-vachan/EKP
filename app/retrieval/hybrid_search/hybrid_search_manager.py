from __future__ import annotations

from app.retrieval.hybrid_search.interfaces.base_hybrid_search import BaseHybridSearch
from app.retrieval.hybrid_search.hybrid_search_registry import HybridSearchRegistry
from app.schemas.search_result import SearchResult
from app.config.config import HybridSearchConfig

class HybridSearchManager:

    def __init__(self, config: HybridSearchConfig) -> None:

        self._config = config

        provider_cls = HybridSearchRegistry.get(
            config.provider
        )
        self._provider = self._create_provider(
            provider_cls
        )
    

    def fuse(self, 
             vector_results: list[SearchResult],
             lexical_result: list[SearchResult],
            ) -> list[SearchResult]:
        
        return self._provider.fuse(
            vector_results = vector_results,
            lexical_result = lexical_result,
        )
    
    
    def _create_provider(self, provider_cls: type[BaseHybridSearch]) -> BaseHybridSearch:
        """
            create the configured provider.
        """

        return provider_cls(self._config)