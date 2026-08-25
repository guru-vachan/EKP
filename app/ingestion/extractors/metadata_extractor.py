from __future__ import annotations

from pathlib import Path

import fitz  # PyMuPDF

from app.schemas.metadata import Metadata
from app.utils.parse_date import parse_pdf_date

class MetaDataExtractor:
    """
        This class responsiable only for metadata extraction.
        
    """

    @staticmethod
    def extract(document: fitz.Document, file_path: Path) -> Metadata:
        """
            Extrsct metadata from an Opened PDF.
            Args:
                document: Open PyMuPDF document
                file_path: Original pdf path

            Return: MetaData object 
        """
        pdf_metadata = document.metadata or {}


        return Metadata(
            title = pdf_metadata.get("title"),
            author = pdf_metadata.get("author"),
            subject= pdf_metadata.get("subject"),
            creator= pdf_metadata.get("creator"),
            producer= pdf_metadata.get("producer"),
            creation_date= parse_pdf_date(pdf_metadata.get("creationDate")),
            modified_date= parse_pdf_date(pdf_metadata.get("modifiedDate")),
            page_count= document.page_count,
            file_size= file_path.stat().st_size,
        )