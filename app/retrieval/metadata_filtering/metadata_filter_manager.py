from __future__ import annotations

from app.config.config import MetadataFilterConfig
from app.retrieval.metadata_filtering.interfaces.base_metadata_filter import BaseMetadataFilter
from app.retrieval.metadata_filtering.metadata_filter_registry import MetadataFilterRegistry
from app.schemas.FilterCriteria import FilterCriteria
from app.schemas.query import Query

class MetadataFilterManager:


    def __init__(self, config: MetadataFilterConfig) -> None:

        self._config = config

        provider_cls = MetadataFilterRegistry.get(
            config.provider
        )
        self._provider = self._create_provider(
            provider_cls
        )
    

    def generate(self, query: Query) -> FilterCriteria:
        """
            generate metadata for the query.
        """

        return self._provider.generate(query)
    

    def _create_provider(self, provider_cls: type[BaseMetadataFilter]) -> BaseMetadataFilter:
        """
            create the configured Metadata filter provider.
        """

        return provider_cls(self._config)