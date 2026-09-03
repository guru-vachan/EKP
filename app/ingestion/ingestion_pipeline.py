from __future__ import annotations

from pathlib import Path
import logging
from time import perf_counter

# These import trigger decorator based provider registraction
import app.embeddings.providers
import app.ingestion.chunking
import app.ingestion.loaders
import app.vectorstore.providers

from app.config.config import (
    ChunkingConfig,
    EmbeddingConfig,
    VectorStoreConfig
)

from app.embeddings.embedding_manager import EmbeddingManager
from app.vectorstore.vectorstore_manager import VectorStoreManager
from app.ingestion.ingestion_manager import IngestionManager
from app.ingestion.chunking.chunking_manager import ChunkingManager
from app.schemas.ingestion_result import IngestionResult
from app.ingestion.state.ingestion_state import IngestionState
from app.ingestion.state.ingestion_status import IngestionStatus
from app.ingestion.metadata.metadata_helper import ( calculate_checksum, build_ingestion_key)

logger = logging.getLogger(__name__)

# Importent
# Dont make this pipeline async, for large ingestion, the eventual archiecture should be:
#   upload API ----> Job Queue
#                       |
#                       |--> worker
#                       |--> worker
#                       |--> worker
#                               |
#                               |
#                          IngestionPipeline


class IngestionPipeline:

    def __init__(self, 
                 ingestion_manager: IngestionManager,
                 chunking_manager: ChunkingManager,
                 embedding_manager: EmbeddingManager,
                 vector_store_manager: VectorStoreManager,
                 ingestion_state: IngestionState,
                 chunking_config: ChunkingConfig,
                 embedding_config: EmbeddingConfig,
                 vector_store_config: VectorStoreConfig,
                 ) -> None:
        
        self._ingestion = ingestion_manager
        self._chunking = chunking_manager
        self._embeddings = embedding_manager
        self._vector_store = vector_store_manager
        self._state = ingestion_state
        self._chunking_config = chunking_config
        self._embedding_config = embedding_config
        self.vector_store_config = vector_store_config

        
    
    def ingest(self, file_path: str | Path) -> IngestionResult:

        path = Path(file_path)

        checksum = calculate_checksum(path)

        ingestion_key = build_ingestion_key( 
            checksum=checksum,
            chunking_strategy=self._chunking_config.strategy,
            chunk_size=self._chunking_config.chunk_size,
            chunk_overlap=self._chunking_config.chunk_overlap,
            embedding_model=self._embedding_config.model_name
        )

        status = self._state.get(ingestion_key)

        if status == IngestionStatus.COMMITTED:
            raise ValueError(
                f"Document already ingested: {path.name}."
            )
        
        self._state.mark(
            ingestion_key,
            IngestionStatus.PROCESSING
        )

        started_at = perf_counter()

        logging.info("Starting ingestion %s", path.name)

        try:
            document = self._ingestion.ingest(path)

            chunks = self._chunking.chunk(document)

            if not chunks:
                raise ValueError(
                    f"No chunks generated for '{path.name}."
                )
            
            embeddings = self._embeddings.encode(chunks)

            if len(embeddings) != len(chunks):
                raise RuntimeError(
                    "Embedding does not match chunks count."
                )
            
            self._vector_store.add(embeddings)
            self._vector_store.persist()

            self._state.mark(
                ingestion_key,
                IngestionStatus.COMMITTED
            )

            elapsed_ms = (
                perf_counter() - started_at
            ) * 1000

            logger.info(
                "Ingestion completed: file= %s "
                "chunks= %d embeddings=%d duration_ms=%.2f",
                path.name,
                len(chunks),
                len(embeddings),
                elapsed_ms
            )

            return IngestionResult(
                document_id=document.document_id,
                file_name=document.file_name,
                chunk_created=len(chunks),
                embedded_created=len(embeddings),
                vector_store=self._vector_store.name,
            )
        
        except Exception:
            self._state.mark(
                ingestion_key,
                IngestionStatus.FAILED
            )
            logger.exception(
                "ingestion failed: %s", path.name,
            )
            raise
            
            
