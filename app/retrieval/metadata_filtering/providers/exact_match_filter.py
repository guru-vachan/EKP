from __future__ import annotations

import re

from app.config.config import MetadataFilterConfig
from app.core.enums import FilterOperator
from app.retrieval.metadata_filtering.interfaces.base_metadata_filter import BaseMetadataFilter
from app.retrieval.metadata_filtering.metadata_filter_registry import MetadataFilterRegistry
from app.schemas.FilterCriteria import FilterCriteria
from app.schemas.query import Query


@MetadataFilterRegistry.register
class ExactMatchFilter(BaseMetadataFilter):
    """
        Rule based meta data filter generator 
    """

    def __init__(self, config: MetadataFilterConfig) -> None:
        super().__init__(config)
    

    @classmethod
    def name(cls) -> str:
        return "exact_match"
    
    def generate(self, query: Query) -> FilterCriteria:
        """
            generate metadata filters from the query.
        """

        filters: list[MetadataFilterConfig] = []

        text = query.query.lower()

        
        # Language
        language_match = re.search(
            r"\b(english|hindi|german)\b",
            text
        )

        if language_match:
            filters.append(
                MetadataFilterConfig(
                    field="language",
                    operator=FilterOperator.EQ,
                    value=language_match.group(1)
                )
            )

        # Document type
        document_type_match = re.search(
            r"\b(pdf|wiki|ppt|docx)\b",
            text
        )

        if document_type_match:
            filters.append(
                MetadataFilterConfig(
                    field="document_type",
                    operator=FilterOperator.EQ,
                    value=document_type_match.group(1)
                )
            )
        
        return FilterCriteria(
            filters=filters
        )
