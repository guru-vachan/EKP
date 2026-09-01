from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from numpy.typing import NDArray
import numpy as np

from app.schemas.embedding import Embedding
from app.schemas.search_result import SearchResult

class BaseVectorStore(ABC):
    """
        Abstract base class for all vectore store providers
    """

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        """
            return provider name.
            eg:
                1. faiss
                2. pinecone
                3. chroma
        """
        raise NotImplementedError
    
    @abstractmethod
    def add(self, embeeding: list[Embedding]) -> None:
        """
            insert embeddngs into vector store.
        """
        raise NotImplementedError
    
    @abstractmethod
    def search(self, query_vector: NDArray[np.float32], top_k: int) -> list[SearchResult]:
        """
            search simier results
        """
        raise NotImplementedError
    
    @abstractmethod
    def persist(self, directory: Path) -> None:
        """
            persist the vector store.
        """
        raise NotImplementedError


    @abstractmethod
    def load(self, directory: Path) -> None:
        """
            load the vector store.
        """
        raise NotImplementedError
    

        