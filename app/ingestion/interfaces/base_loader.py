from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from app.schemas.document import Document

class BaseLoader(ABC):
    """
    
    Abstract base class for all document  loaders.

    Every loader is responsiable for:
        1. Validating the input file.
        2. Loading the document.
        3. Returing a standardized Document object.

    Supported implementations:
        - PDFLoader
        - WikiLoader
        - ConflunceLoader etc....

    """

    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)

    
    @abstractmethod
    def validate(self) -> None:
        """
        
        Validate the input file before processing.

        Raises:
            FileNotFoundError: if file does not exist.

            InvalidFileError: if file type not supported.

            PermissionError: if the application cannot access the file
    
        """
        raise NotImplementedError
    

    @abstractmethod
    def supports(self) -> tuple[str, ...]:
        """
            Return support file extensions eg: pdf, etc...

            A small abstruction can eliminate futute conditional logic and imporve extensibility
        """
    
    
    def load(self) -> Document:
        """
        
        Load the document and return a standardized Document object.

        Returns: Document

        Raises:
            IngestionError: if document loading fails

        """
        raise NotImplementedError
