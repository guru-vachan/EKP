from __future__ import annotations

from app.schemas.query import Query
from app.config.config import QueryRewriteConfig

from app.retrieval.query_rewriting.interfaces.base_query_rewriter import (
    BaseQueryRewriter
)
from app.retrieval.query_rewriting.query_rewriter_registry import (
    QueryRewriterRegistry
)

class QueryRewriterManager:
    """

    """

    def __init__(self, config: QueryRewriteConfig) -> None:

        self._config = config

        provider_cls = QueryRewriterRegistry.get(
            config.provider
        )
        self._provider = self._create_provider(
            provider_cls
        )

    
    def rewrite(self, query: Query) -> Query:
        """
            Rewrite the query.
        """

        return self._provider.rewrite(query)
    

    def _create_provider(self, provider_cls: type[BaseQueryRewriter]) -> BaseQueryRewriter:
        """
            create the configured provider.
        """

        return provider_cls(self._config)