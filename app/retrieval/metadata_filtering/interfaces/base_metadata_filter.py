from __future__ import annotations

from abc import ABC, abstractmethod

from app.schemas.query import Query
from app.config.config import MetadataFilterConfig
from app.schemas.FilterCriteria import FilterCriteria


class BaseMetadataFilter(ABC):
    """
        A metadata filter provider analyzes a query and generates
        structured filter critria. it does not execute the filter.
    """

    def __init__(self, config: MetadataFilterConfig) -> None:

        self._config = config
    

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        """
            return Metadata filter provider name
            eg:
                1. exact_match
                2. llm
        """
        raise NotImplementedError
    
    @abstractmethod
    def generate(self, query: Query) -> FilterCriteria:
        """
            Args: processed user query.

            return: structured filter critria. because this component does not filter documents.
                    Retriver/Hybrid Search layer will consume FilterCriteria and decide HOW to apply it.
        """
        raise NotImplementedError