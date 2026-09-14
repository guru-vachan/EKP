from __future__ import annotations

from app.config.config import LexicalSearchConfig
from app.schemas.search_result import SearchResult
from app.schemas.FilterCriteria import FilterCriteria

from app.retrieval.lexical_search.lexical_search_registry import LexicalSearchRegistry
from app.retrieval.lexical_search.interfaces.base_lexical_search import BaseLexicalSearch

from app.schemas.query import Query

class LexicalSearchManager:

    def __init__(self, config: LexicalSearchConfig) -> None:

        self._config = config

        provider_cls = LexicalSearchRegistry.get(
            config.provider
        )
        self._provider = self._create_provider(
            provider_cls
        )
    

    def search(self, query: Query, filters: FilterCriteria,) -> list[SearchResult]:

        return self._provider.search(query, filters)
    

    def _create_provider(self, provider_cls: type[BaseLexicalSearch]) -> BaseLexicalSearch:
        """
            create the configured provider.
        """

        return provider_cls(self._config)