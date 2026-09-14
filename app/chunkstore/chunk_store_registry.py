from __future__ import annotations

from app.core.registry import Registry
from app.chunkstore.intefaces.base_chunk_store import BaseChunkStore


ChunkStoreRegistry = Registry[BaseChunkStore]()