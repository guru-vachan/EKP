from __future__ import annotations

from app.ingestion.interfaces.base_loader import BaseLoader
from app.core.exceptions import UnsupportedFileTypeError

class LoaderRegistry:
    """
    
        This creates an empty dictionary:

        key   → str
        value → a class that inherits from BaseLoader class not an Object
    """

    """
        Learning Note: 
            _         →    leading _ tells other developers, Don't access this directly from outside the class; use the class's public methods.
            loaders   →     descriptive name
            lowercase →     mutable attribute, not a constant
    """
    _loaders: dict[str, type[BaseLoader]] = {}

    @classmethod
    def register(cls, loader_cls: type[BaseLoader]) -> None:
        """
            return:
                {
                    ".pdf": PDFLoader,
                    ".docx": DOCXLoader,
                    ".txt": TXTLoader
                }
        """
        for extension in loader_cls.supports():
            cls._loaders[extension] = loader_cls

        return loader_cls

    @classmethod
    def get(cls, extension: str) -> type[BaseLoader]:

        try:
            return cls._loaders[extension.lower()]
        except KeyError:
            raise UnsupportedFileTypeError(
                f"Unsupported file type: '{extension}'"
            )