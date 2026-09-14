from pydantic import BaseModel, ConfigDict

from app.config.config import (
    ChunkingConfig,
    EmbeddingConfig,
    VectorStoreConfig,
    QueryConfig,
    QueryRewriteConfig,
    MetadataFilterConfig,
    ChunkStoreConfig,
    LexicalSearchConfig,
    HybridSearchConfig
)

class TestEnvironment(BaseModel):

    model_config = ConfigDict( frozen=True, extra="forbid" )

    query_config: QueryConfig
    query_rewrite_config: QueryRewriteConfig
    metadata_filter_config: MetadataFilterConfig

    chunking_config: ChunkingConfig
    embedding_config: EmbeddingConfig

    vector_store_config: VectorStoreConfig
    chunk_store_config: ChunkStoreConfig

    lexical_search_config: LexicalSearchConfig
    hybrid_search_config: HybridSearchConfig

    
