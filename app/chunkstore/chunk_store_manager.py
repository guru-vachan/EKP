from __future__ import annotations

from pathlib import Path

from app.schemas.chunk import Chunk
from app.chunkstore.intefaces.base_chunk_store import BaseChunkStore
from app.chunkstore.chunk_store_registry import ChunkStoreRegistry
from app.config.config import ChunkStoreConfig

class ChunkStoreManager:
    """
    Manager responsible for selecting and delegating to
    the configured chunk store provider.
    """

    def __init__(self, config: ChunkStoreConfig) -> None:

        self._config = config

        provider_cls = ChunkStoreRegistry.get(
            config.provider
        )
        self._provider = self._create_provider(
            provider_cls
        )
    

    def add(self, chunks: list[Chunk]) -> None:
        """
        Add multiple chunks to the store.
        """
        self._provider.add(chunks)

    def get(self, chunk_id: str) -> Chunk | None:
        """
        Retrieve a single chunk by its ID.
        """
        return self._provider.get(chunk_id)

    def get_many(self, chunk_ids: list[str]) -> list[Chunk]:
        """
        Retrieve multiple chunks by their IDs.
        """
        return self._provider.get_many(chunk_ids)

    def exists(self, chunk_id: str) -> bool:
        """
        Check whether a chunk exists in the store.
        """
        return self._provider.exists(chunk_id)
    
    
    def delete(self, document_id: str) -> bool:
        """
        Check whether a chunk exists in the store.
        """
        return self._provider.delete(document_id)
    

    def _create_provider(self, provider_cls: type[BaseChunkStore]) -> BaseChunkStore:
        """
            create the configured provider.
        """

        return provider_cls(self._config)