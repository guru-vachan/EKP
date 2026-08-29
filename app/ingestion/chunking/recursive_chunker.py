from __future__ import annotations

import logging
from uuid import uuid4

from app.schemas.chunk import Chunk
from app.config.config import ChunkingConfig
from app.ingestion.chunking.interfaces.base_chunker import BaseChunker
from app.ingestion.chunking.text_splitter_factory import TextSplitterFactory
from app.schemas.document import Document
from app.ingestion.chunking.chunker_register import ChunkerRegistry

logger = logging.getLogger(__name__)


@ChunkerRegistry.register
class RecursiveChunker(BaseChunker):
    """
        Recursive chunking implementation.
    """

    def __init__(self, config: ChunkingConfig) -> None:
        self._config = config

        self._splitter = TextSplitterFactory.create(
            strategy="recursive",
            config=config,
        )
    

    @classmethod
    def name(cls) -> str:
        return "recursive"
    
    def split(self, document: Document) -> list[Chunk]:

        logger.info(
            "Chunking document '%s'", document.file_name
        )

        texts = self._splitter.split_text(document.content)

        chunks: list[Chunk] = []

        for index, text in enumerate(texts):

            chunks.append(
                Chunk(
                    chunk_id=str(uuid4()),
                    document_id=document.document_id,
                    chunk_index=index,
                    content=text,
                    metadata=document.metadata,
                    character_count=len(text),
                )
            )
        
        logger.info(
            "Generated %d Chunks", len(chunks)
        )

        return chunks