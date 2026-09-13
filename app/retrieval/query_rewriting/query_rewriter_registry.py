from __future__ import annotations

from app.core.registry import Registry
from app.retrieval.query_rewriting.interfaces.base_query_rewriter import BaseQueryRewriter


QueryRewriterRegistry = Registry[BaseQueryRewriter]()