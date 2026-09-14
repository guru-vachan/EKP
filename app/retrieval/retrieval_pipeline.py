from __future__ import annotations

import logging

from app.embeddings.embedding_manager import EmbeddingManager
from app.retrieval.hybrid_search.hybrid_search_manager import HybridSearchManager
from app.retrieval.lexical_search.lexical_search_manager import LexicalSearchManager
from app.retrieval.metadata_filtering.metadata_filter_manager import MetadataFilterManager
from app.retrieval.query_processing.query_processor import QueryProcessor
from app.retrieval.query_rewriting.query_rewriting_manager import QueryRewriterManager
from app.vectorstore.vectorstore_manager import VectorStoreManager
from app.chunkstore.chunk_store_manager import ChunkStoreManager

from app.schemas.chunk import Chunk
from app.schemas.search_result import SearchResult

logger = logging.getLogger(__name__)

class RetrievalPipeline:

    def __init__(
        self,
        query_processor: QueryProcessor,
        query_rewriter: QueryRewriterManager,
        metadata_filter: MetadataFilterManager,
        embedding: EmbeddingManager,
        vector_store: VectorStoreManager,
        chunk_store: ChunkStoreManager,
        lexical_search: LexicalSearchManager,
        hybrid_search: HybridSearchManager,

    ) -> None:
        
        self._embedding = embedding
        self._hybrid_search= hybrid_search
        self._lexical_search = lexical_search
        self._metadata_filter = metadata_filter
        self._query_processor = query_processor
        self._query_rewriter = query_rewriter
        self._vector_store = vector_store
        self._chunk_store = chunk_store

    
    def retrieve(self, query: str) -> list[SearchResult]:

        logging.info("Starting retrieve pipeline")

        # --------------------------------------------------
        # 1. Query Processing
        # --------------------------------------------------
        processed_query = self._query_processor.process(query)

        # --------------------------------------------------
        # 2. Query Rewriting
        # --------------------------------------------------
        rewritten_query = self._query_rewriter.rewrite(
            processed_query
        )

        # --------------------------------------------------
        # 3. Metadata Filtering
        # --------------------------------------------------
        filters = self._metadata_filter.generate(
            rewritten_query
        )

        # --------------------------------------------------
        # 4. Generate Query Embedding
        # --------------------------------------------------
        query_embedding = self._embedding.encode(
            rewritten_query.query
        )

        # --------------------------------------------------
        # 5. Vector Search
        # --------------------------------------------------
        vector_results = self._vector_store.search(
            query_vector=query_embedding,
        )

        # --------------------------------------------------
        # 4. Load Chunks
        # --------------------------------------------------
        chunk_map = {
            
            chunk.chunk_id: chunk
            for chunk in self._chunk_store.get_many(
                [
                    result.chunk_id
                    for result in vector_results
                ]
            )
        }

        vector_results = [
            result.model_copy(
                update={
                    "chunk": chunk_map[
                        result.chunk_id
                    ]
                }
            )
            for result in vector_results
        ]

        # --------------------------------------------------
        # 6. Lexical Search
        # --------------------------------------------------
        lexical_results = self._lexical_search.search(
            query=rewritten_query,
            filters=filters,
        )

        # --------------------------------------------------
        # 7. Hybrid Search / Ranking
        # --------------------------------------------------
        results = self._hybrid_search.fuse(
            vector_results=vector_results,
            lexical_results=lexical_results,
        )

        logging.info("Retrieved %d chunks.", len(results))

        return results