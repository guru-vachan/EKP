from __future__ import annotations

from app.config.config import ChunkingConfig
from app.ingestion.chunking.chunker_register import ChunkerRegistry
from app.schemas.chunk import Chunk
from app.schemas.document import Document

class ChunkingManager:

    def __init__(self, config: ChunkingConfig) -> None:
        self._config = config
    

    def chunk(self, document: Document) -> list[Chunk]:

        chunker_cls = ChunkerRegistry.get(self._config.strategy.value)

        chunker = chunker_cls(self._config)

        return chunker.split(document)