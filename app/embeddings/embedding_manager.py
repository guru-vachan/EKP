from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from app.config.config import EmbeddingConfig
from app.embeddings.embedding_registry import EmbeddingRegistry
from app.schemas.chunk import Chunk
from app.schemas.embedding import Embedding

class EmbeddingManager:
    """
        Orchestrates embedding generation.
    """

    def __init__(self, config: EmbeddingConfig) -> None:

        self._config = config
        
        provider_cls = EmbeddingRegistry.get(config.provider.value)
        self._provider = provider_cls(config)
        
    
    def encode(self, chunks: list[Chunk]) -> list[Embedding]:

        return self._provider.encode(chunks)
    
    def encode_query(self, query: str) -> NDArray[np.float32]:

        return self._provider.encode_query(query)