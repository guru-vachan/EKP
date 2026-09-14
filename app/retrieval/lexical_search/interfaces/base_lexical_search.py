from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from app.config.config import LexicalSearchConfig
from app.schemas.search_result import SearchResult
from app.schemas.FilterCriteria import FilterCriteria
from app.schemas.query import Query
from app.schemas.chunk import Chunk

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
    
    @abstractmethod
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
    
    @abstractmethod
    def build(self, chunks: list[Chunk]) -> None:
        return NotImplementedError
    
    @abstractmethod
    def persist(self) -> None:
        return NotImplementedError

    @abstractmethod
    def load(self) -> None:
        return NotImplementedError