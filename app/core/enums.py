from __future__ import annotations

from enum import Enum

class ChunkingStrategy(str, Enum):

    RECURRSIVE = "recurrsive"
    SEMANTIC = "semantic"


class EmbeddingProvider(str, Enum):

    BGE = "bge"
    E5 = "e5"


class VectorStoreProvider(str, Enum):

    FAISS = "faiss"
    PINECONE = "pinecone"
    CHORMA = "chorma"


class IndexType(str, Enum):

    FLAT_L2 = "flat_l2"
    FLAT_IP = "flat_ip"
    HNSW = "hnsw"


class FilterOperator(str, Enum):

    EQ = "eq"
    GTE = "gte"
    LTE = "lte"