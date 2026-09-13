from __future__ import annotations

from app.core.registry import Registry
from app.ingestion.interfaces.base_loader import BaseLoader
from app.core.exceptions import UnsupportedFileTypeError


LoaderRegistry = Registry[BaseLoader]()