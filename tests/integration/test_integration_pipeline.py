from __future__ import annotations

from pathlib import Path 

import numpy as np 
import pytest

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

@pytest.mark.integration
def test_pdf_to_faiss_end_to_end(
        tmp_path: Path,
) -> None:
    
    pdf_path = Path("data/raw/sample.pdf")

    assert pdf_path.exists(), (
        f"Integration fixture not found: {pdf_path}"
    )

    chunking_config = ChunkingConfig(
        strategy="recursive",
        chunk_size=500,
        chunk_overlap=100
    )

    embedding_config = EmbeddingConfig(
        provider="bge", 
        model_name="BAAI/bge-small-en-v1.5", 
        device="cpu", 
        batch_size=16, 
        normalize_embeddings=True, 
    )

    vector_store_config = VectorStoreConfig( 
            provider="faiss", 
            dimension=384, 
            index_type="flat_ip", 
            top_k=3, 
            storage_directory= tmp_path / "vector_store", 
        )
    
    # ---------------------
    # Ingestion
    # ---------------------

    ingestion_manager = IngestionManager()

    document = IngestionManager.ingest(pdf_path)

    assert document.document_id
    assert document.content.strip()
    assert document.file_name == pdf_path.name
    assert document.metadata.page_count > 0

    # ---------------------
    # Chunking
    # ---------------------

    chunking_manager = ChunkingManager(chunking_config)

    chunks = chunking_manager.chunk(document)

    assert chunks
    assert all(
        chunk.document_id == document.document_id
        for chunk in chunks
    )
    assert all(
        chunk.content.strip()
        for chunk in chunks
    )
    chunk_ids = {
        chunk.chunk_id
        for chunk in chunks
    }
    assert len(chunk_ids) == len(chunks)

    # ---------------------------
    # Embedding Generation
    # ----------------------------

    embedding_manager = EmbeddingManager(embedding_config) 

    embeddings = embedding_manager.encode(chunks) 

    assert len(embeddings) == len(chunks)
    assert all(
        embedding.chunk_id in chunk_ids
        for embedding in embeddings
    )
    assert all(
        embedding.dimension == vector_store_config.dimension
        for embedding in embeddings
    )
    assert all(
        embedding.vector.dtype == np.float32
        for embedding in embeddings
    )

    # ---------------------------
    # Store in FAISS
    # ----------------------------

    vector_store = VectorStoreManager(vector_store_config) 

    vector_store.initialize()
    vector_store.add(embeddings)
    vector_store.persist()

    index_path = (
        Path(vector_store_config.storage_directory)
        / "faiss.index"
    )

    mapping_path = (
        Path(vector_store_config.storage_directory)
        / "index_to_chunk_id.json"
    )

    assert index_path.exists()
    assert mapping_path.exists()

    # ---------------------------
    # Reload into a New Vector-Store instance
    # ----------------------------

    reloaded_store = VectorStoreManager(
        vector_store_config
    )

    reloaded_store.initialize()

    # ---------------------------
    # create query embedding
    # ----------------------------


    # for initaial we reuse one document chunk as the query.
    # After will intoduce a dedicated encode_query() API.
    query_embeddings = embedding_manager.encode(
        [chunks[0]]
    )
    assert len(query_embeddings) == 1

    query_vector = query_embeddings[0].vector

    # ---------------------------
    # Search
    # ----------------------------

    results = reloaded_store.search(
        query_vector
    )

    # ---------------------------
    # Validate Retrieval
    # ----------------------------

    assert results
    assert len(results) <= vector_store_config.top_k
    assert all(
        result.vector_store == "faiss"
        for result in results
    )
    assert all(
        result.chunk_id in chunk_ids
        for result in results
    )
    assert [
        result.rank
        for result in results
    ] == list(
        range(1, len(results) + 1)
    )

    # Because we are quering with chunk[0]'s own vector
    # it should normally be the nearest result.
    assert results[0].chunk_id == chunks[0].chunk_id