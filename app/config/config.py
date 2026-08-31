from pydantic import BaseModel

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