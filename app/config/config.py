from pydantic import BaseModel, ConfigDict, Field

from app.enum.index_type import IndexType

class ChunkingConfig(BaseModel):
    chunk_size: int = 1000
    chunk_overlap: int = 200
    strategy: str


class EmbeddingConfig(BaseModel):
    device: str
    model_name: str
    normalize_embeddings: str
    batch_size: int
    provider: str | None = "bge"


class VectorStoreConfig(BaseModel):
    model_config = ConfigDict(
        frozen=True
    )
    provider: str
    dimension: int = Field(
        gt=0
    )
    index_type: IndexType
    hnsw_m: int = 32
    top_k: int = 5
    persist_directory: str = (
        "data/vector_store"
    )