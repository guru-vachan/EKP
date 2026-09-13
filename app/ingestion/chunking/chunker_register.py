from __future__ import annotations

from app.core.registry import Registry
from app.ingestion.chunking.interfaces.base_chunker import BaseChunker
from app.core.exceptions import UnsupportedChunkingStrategy


ChunkerRegistry = Registry[BaseChunker]()