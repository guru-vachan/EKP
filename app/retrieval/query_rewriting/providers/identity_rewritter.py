from __future__ import annotations

from app.schemas.query import Query
from app.config.config import QueryRewriteConfig

from app.retrieval.query_rewriting.interfaces.base_query_rewriter import (
    BaseQueryRewriter
)
from app.retrieval.query_rewriting.query_rewriter_registry import (
    QueryRewriterRegistry
)


@QueryRewriterRegistry.register
class IdentityRewriter(BaseQueryRewriter):
    """
        Default query registry

        Returns the original processed query without modification / no-LLM baseline. it is useful for testing
    """

    def __init__(self, config: QueryRewriteConfig) -> None:
        super().__init__(config)

    
    @classmethod
    def name(cls) -> str:
        return "identity"
    

    def rewrite(self, query: Query) -> Query:
        """
            return the original query.
        """
        return query.model_copy(
            update={
                "rewritten": False
            }
        )