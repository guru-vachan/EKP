from __future__ import annotations

import logging
from uuid import uuid4

from app.schemas.chunk import Chunk
from app.config.config import ChunkingConfig
from app.ingestion.chunking.interfaces.base_chunker import BaseChunker
from app.schemas.document import Document
from app.ingestion.chunking.chunker_register import ChunkerRegistry

logger = logging.getLogger(__name__)

@ChunkerRegistry.register
class SemanticChunker(BaseChunker):
    """
        Sementic chunking implementation.
    """

    def __init__(self, config: ChunkingConfig) -> None:
        self._config = config
    

    @classmethod
    def name(cls) -> str:
        return "sementic"
    
    def split(self, document: Document) -> list[Chunk]:
        raise NotImplementedError(
            "Semantic chunking will be implemented later during embedding."
        )