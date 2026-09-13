from __future__ import annotations

from abc import ABC, abstractmethod

from app.config.config import HybridSearchConfig
from app.schemas.search_result import SearchResult

class BaseHybridSearch(ABC):
    """
        Hybrid search does not perform search. it just merge multiple
        ranked result into a single ranking.
    """
    def __init__(self, config: HybridSearchConfig) -> None:
        self._config = config
    

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        """
            return strategy name
            eg:
                1. RRF
                2. Weight fusion
        """
        raise NotImplementedError
    

    def fuse(self, 
             vector_results: list[SearchResult],
             lexical_result: list[SearchResult],
            ) -> list[SearchResult]:
        """
        Args:
            vector_results: result return by vector search

            lexical_result: result return by lexical search
        """
        return NotImplementedError