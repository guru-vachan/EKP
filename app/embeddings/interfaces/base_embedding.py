from __future__ import annotations

from abc import ABC, abstractmethod

from app.schemas.embedding import Embedding
from app.schemas.chunk import Chunk

class BaseEmbedding(ABC):


    @classmethod
    @abstractmethod
    def name(cls) -> str:
        """
            return embedding provide name 
            eg:
                bge-small, e5-base, text-embedding-3-small
        """
        raise NotImplementedError
    
    def encode(self, chunks: list[Chunk],) -> list[Embedding]:
        """
            Generate embeddings for chunks. 
            Every embeddings library uses encode. 
            eg:
                SentenseTransformer.encode()
                FlagEmbedding.encode()

        """
        raise NotImplementedError