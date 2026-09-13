from __future__ import annotations

from abc import ABC, abstractmethod

from app.schemas.query import Query
from app.config.config import QueryRewriteConfig

class BaseQueryRewriter(ABC):
    """
        abstract base class for all query rewritter.
    """

    def __init__(self, config: QueryRewriteConfig) -> None:

        self._config = config

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        """
            return query rewritter name
            eg:
                1. gemini
                2. identity
        """

        raise NotImplementedError
    

    @abstractmethod
    def rewrite(self, query: Query) -> Query:
        """
            Args: processed query.

            return: rewritten query.
        """

        raise NotImplementedError