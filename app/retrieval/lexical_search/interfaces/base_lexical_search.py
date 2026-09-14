from __future__ import annotations

from abc import ABC, abstractmethod

from app.config.config import LexicalSearchConfig
from app.schemas.search_result import SearchResult
from app.schemas.FilterCriteria import FilterCriteria
from app.schemas.query import Query

class BaseLexicalSearch(ABC):

    def __init__(self, config: LexicalSearchConfig) -> None:
        self._config = config
    

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        """
            return strategy name
            eg:
                1. bm25
                2. elastic search 
                3. Opensearch
        """
        raise NotImplementedError
    

    def search(self, 
             query: Query,
             filters: FilterCriteria,
            ) -> list[SearchResult]:
        """
        Args:
            query: processed query

            filters: Metadata filters
        
            Return:
                ranked search results
        """
        return NotImplementedError