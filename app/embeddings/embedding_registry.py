from __future__ import annotations

from app.core.registry import Registry
from app.embeddings.interfaces.base_embedding import BaseEmbedding
from app.core.exceptions import UnsupportedEmbeddingProvider


EmbeddingRegistry = Registry[BaseEmbedding]()