from __future__ import annotations

from app.core.registry import Registry
from app.vectorstore.interface.base_vectorstore import BaseVectorStore
from app.core.exceptions import UnsupportedVectorStoreProvider


VectorStoreRegistry = Registry[BaseVectorStore]()