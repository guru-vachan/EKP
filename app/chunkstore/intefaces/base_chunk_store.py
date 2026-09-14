from __future__ import annotations

from abc import ABC, abstractmethod

from app.config.config import ChunkStoreConfig
from app.schemas.chunk import Chunk

class BaseChunkStore(ABC):

    def __init__(self, config: ChunkStoreConfig) -> None:
        self._config = config

    
    @classmethod
    @abstractmethod
    def name(cls) -> str:
        raise NotImplementedError
    

    @abstractmethod
    def add(self, chunks: list[Chunk]) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def get(self, chunk_id: str) -> Chunk | None:
        raise NotImplementedError
    
    @abstractmethod
    def get_many(self, chunk_ids: list[str]) -> list[Chunk]:
        raise NotImplementedError
    
    @abstractmethod
    def exists(self, chunk_id: str) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, document_id: str) -> None:
        raise NotImplementedError