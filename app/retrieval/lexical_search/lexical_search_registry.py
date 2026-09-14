from __future__ import annotations

from app.core.registry import Registry
from app.retrieval.lexical_search.interfaces.base_lexical_search import BaseLexicalSearch


LexicalSearchRegistry = Registry[BaseLexicalSearch]()