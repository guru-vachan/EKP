from __future__ import annotations

from app.core.registry import Registry
from app.retrieval.hybrid_search.interfaces.base_hybrid_search import BaseHybridSearch


HybridSearchRegistry = Registry[BaseHybridSearch]()