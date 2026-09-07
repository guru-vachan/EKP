from __future__ import annotations

from numpy.typing import NDArray
from pathlib import Path

from app.config.config import VectorStoreConfig
from app.schemas.embedding import Embedding
from app.schemas.search_result import SearchResult
from app.vectorstore.vectorstore_registry import VectorStoreRegistry

class VectorStoreManager:

    def __init__(self, config: VectorStoreConfig) -> None:

        self._config = config

        provider_cls = VectorStoreRegistry.get(config.provider.value)

        self._provider = provider_cls(config)

    
    def add(self, embeddings: list[Embedding]) -> None:

        self._provider.add(embeddings)


    def search(self, query_vector: NDArray) -> list[SearchResult]:

        return self._provider.search(
            query_vector=query_vector,
            top_k=self._config.top_k,
        )
    
    def initialize(self) -> None:

        index_path = (
            Path(self._config.storage_directory)
            / "faiss.index"
        )

        if index_path.exists():
            self._provider.load(
                self._config.storage_directory
            )
    
    def persist(self) -> None:

        self._provider.persist(
            self._config.storage_directory
        )
    
    @property
    def name(self) -> str:
        return self._provider.name()
