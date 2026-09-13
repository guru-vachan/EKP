from __future__ import annotations

from app.core.registry import Registry
from app.retrieval.metadata_filtering.interfaces.base_metadata_filter import BaseMetadataFilter


MetadataFilterRegistry = Registry[BaseMetadataFilter]()