from __future__ import annotations

import logging
from uuid import uuid4

import numpy as np
from sentence_transformers import SentenceTransformer

from app.config.config import EmbeddingConfig
from app.embeddings.embedding_registry import EmbeddingRegistry
from app.embeddings.interfaces.base_embedding import BaseEmbedding
from app.schemas.chunk import Chunk
from app.schemas.embedding import Embedding

logger = logging.getLogger(__name__)


@EmbeddingRegistry.register
class BGEEmbedding(BaseEmbedding):
    """
        BAAI BGE embedding provider.
    """

    _model: SentenceTransformer | None = None

    def __init__(self, config: EmbeddingConfig) -> None:
        """
            Model loading is expensive (2-5 seconds).
        """

        self._config = config

        if self.__class__._model is None:
            self.__class__._model = SentenceTransformer(
                model_name_or_path=config.model_name,
                device=config.device
            )

        self._model = self.__class__._model

    
    @classmethod
    def name(cls) -> str:
        return "bge"
    

    def encode(self, chunks: list[Chunk]) -> list[Embedding]:
        """
            Generate embedding for chunks.
        """

        if not chunks:
            return []
        
        texts = [
            chunk.content
            for chunk in chunks
        ]

        vectors = self._model.encode(
            texts,
            batch_size=self._config.batch_size,
            normalize_embeddings=self._config.normalize_embeddings,
            convert_to_numpy=True,
            show_progress_bar=False,
        )

        embeddings: list[Embedding] = []

        for chunk, vector in zip(chunks, vectors):

            embeddings.append(
                Embedding(
                    embedding_id=str(uuid4()),
                    chunk_id=chunk.chunk_id,
                    model_name=self._config.model_name,
                    dimension=vector.shape[0],
                    vector = vector.astype(np.float32),

                )
            )
        
        logger.info("Generated %d embedding using %d", len(embeddings), self._config.model_name)

        return embeddings
        
