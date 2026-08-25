from __future__ import annotations

from pathlib import Path

from app.core.exceptions import UnsupportedFileTypeError
from app.ingestion.interfaces.base_loader import BaseLoader
from app.ingestion.loaders.pdf_loader import PDFLoader
from app.schemas.document import Document


class IngestionManager:
    """
    
        Routes a document to the appropriate loader.

        The manager does not know how a document is loaded.
        It only select the correct loader based on the file extension.
    """

    _LOADERS: tuple[type[BaseLoader], ...] = (
        PDFLoader,
       # DOCXLODER, : IN FUTURE IF ADD DOCX LOADER
    )

    @classmethod
    def ingest(cls, file_path: str | Path) -> Document:
        """
        
            Ingest a document and return Standerarized Document object
        """

        file_path = Path(file_path)

        extension = file_path.suffix.lower()

        for loader_cls in cls._LOADERS:

            if extension in loader_cls.supports():
                loader = loader_cls(file_path)
                return loader.load()
            
        raise UnsupportedFileTypeError(
            f"Unsupported file type: '{extension}'"
        )