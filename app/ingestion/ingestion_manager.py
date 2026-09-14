from __future__ import annotations

from pathlib import Path

from app.core.exceptions import UnsupportedFileTypeError
from app.ingestion.interfaces.base_loader import BaseLoader
from app.ingestion.loaders.pdf_loader import PDFLoader
from app.schemas.document import Document
from app.ingestion.loader_registry import LoaderRegistry


class IngestionManager:
    """
    
        Routes a document to the appropriate loader.

        The manager does not know how a document is loaded.
        It only select the correct loader based on the file extension.
    """

    @classmethod
    def ingest(cls, file_path: str | Path) -> Document:
        """

            Ingest a document and return Standerarized Document object.
        """

        file_path = Path(file_path)
        extension = file_path.suffix.lower()

        print("LoaderRegistry")
        print(LoaderRegistry.registered_providers())

        try:
            loader_cls = LoaderRegistry.get(extension)
            loader = loader_cls(file_path)
            print(loader_cls)
            return loader.load()
        except Exception as ex:    
            raise UnsupportedFileTypeError(
                f"Unsupported file type: '{extension}'"
            )