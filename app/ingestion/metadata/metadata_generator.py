from __future__ import annotations

from pathlib import Path

import fitz  # PyMuPDF

from app.ingestion.metadata.metadata_helper import (
    calculate_checksum,
    estimate_character_count,
    estimate_word_count,
    get_file_extension,
    get_file_name,
    get_file_size,
    normalize_string
)
from app.schemas.metadata import Metadata
from app.utils.parse_date import parse_pdf_date

class MetadataGenerator:
    """
        This class responsiable only for metadata extraction.
        
    """

    @staticmethod
    def generate(*, document: fitz.Document, file_path: Path, text: str) -> Metadata:
        """
            Extrsct metadata from an Opened PDF.
            Args:
                document: Open PyMuPDF document
                file_path: Original pdf path
                content drived metadata

            Return: MetaData object 
        """
        pdf_metadata = document.metadata or {}


        return Metadata(
            title = normalize_string(pdf_metadata.get("title")),
            author = normalize_string(pdf_metadata.get("author")),
            subject= normalize_string(pdf_metadata.get("subject")),
            creator= normalize_string(pdf_metadata.get("creator")),
            producer= normalize_string(pdf_metadata.get("producer")),
            creation_date= parse_pdf_date(pdf_metadata.get("creationDate")),
            modified_date= parse_pdf_date(pdf_metadata.get("moDate")),

            #---------- File -----------------
            file_name=get_file_name(file_path),
            file_extension=get_file_extension(file_path),
            checksum=calculate_checksum(file_path),
            file_size= get_file_size(file_path),

            #---------- Document -----------------
            page_count= document.page_count,
            character_count=estimate_character_count(text),
            word_count=estimate_word_count(text)
            
        )