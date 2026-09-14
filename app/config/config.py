from pydantic import BaseModel, ConfigDict, Field, model_validator

from pathlib import Path

from app.core.enums import (
    ChunkingStrategy,
    EmbeddingProvider,
    VectorStoreProvider,
    IndexType,
    FilterOperator,
    ChunkStoreProvider,
)

class ChunkingConfig(BaseModel):
    model_config = ConfigDict(
        # immutable after creation
        frozen=True, 
        # Don't allow fields that aren't defined in the schema.
        extra="forbid"
    )
    chunk_size: int = Field(
        default=1000,
        gt=0
    )
    chunk_overlap: int = Field(
        default=200,
        ge=0
    )
    strategy: ChunkingStrategy = ChunkingStrategy.RECURRSIVE

    @model_validator(mode="after")
    def validate_chunking(self) -> "ChunkingConfig" :

        if self.chunk_overlap >= self.chunk_size:
            raise ValueError(
                "chunk overlap must be smaller than chunk size."
            )
        
        return self


class EmbeddingConfig(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid"
    )
    device: str = "cpu"
    model_name: str = (
        "BAAI/bge-small-en-v1.5"
    )
    normalize_embeddings: bool = True
    batch_size: int = Field(
        default=32,
        gt=0
    )
    provider: EmbeddingProvider | None = EmbeddingProvider.BGE


class VectorStoreConfig(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid"
    )
    provider: VectorStoreProvider = (
        VectorStoreProvider.FAISS
    )
    dimension: int = Field(
        gt=0
    )
    index_type: IndexType = (
        IndexType.FLAT_IP
    )
    hnsw_m: int = Field(
        default=32,
        gt=0
    )
    top_k: int = Field(
        default=5,
        gt=0
    )
    storage_directory: Path = Path(
        "data/vector_store"
    )


class QueryConfig(BaseModel):
    """
        query processing configuration.
    """
    model_config = ConfigDict(
        frozen=True,
    )
    max_query_length: int = Field(
        default=1000,
        gt=0
    )
    min_query_length: int = Field(
        default=1,
        gt=0
    )
    preserve_case: bool = True


class QueryRewriteConfig(BaseModel):

    model_config = ConfigDict(
        frozen=True,
    )
    provider: str

    model_name: str

    temperature: float

    max_tokens: int

    system_prompt: str


class MetadataFilterConfig(BaseModel):
    field: str
    operator: FilterOperator
    value: str | int | float | bool

class HybridSearchConfig(BaseModel):
    # rrf rank-based, not score-based strategy
    provider: str = "rrf"
    rrf_k: int = 60

class LexicalSearchConfig(BaseModel):
    # rrf rank-based, not score-based strategy
    provider: str = "rrf"
    rrf_k: int = 60

class ChunkStoreConfig(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    provider: ChunkStoreProvider = (
        ChunkStoreProvider.SQLITE
    )
    storage_directory: Path = Field(
        default="data/chunk_store/chunks.db"
    )