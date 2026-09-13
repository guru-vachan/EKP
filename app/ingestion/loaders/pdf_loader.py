from __future__ import annotations

import logging
from pathlib import Path
from uuid import uuid4

import fitz  # PyMuPDF

from app.ingestion.metadata.metadata_generator import MetadataGenerator
from app.ingestion.extractors.text_extractor import TextExtractor
from app.ingestion.interfaces.base_loader import BaseLoader
from app.schemas.document import Document
from app.ingestion.loader_registry import LoaderRegistry
from app.core.exceptions import (DocumentLoadingError, UnsupportedFileTypeError)

logger = logging.getLogger(__name__)


"""

    decorator syntax: @LoaderRegistry.register
    meaning at the end it add this line : 
        PDFLoader = LoaderRegistry.register(PDFLoader)

    when it call:
        usually when the module imported eg: 
            if any class contain import PDFLoader its mean register call otherwise not.
         
"""
@LoaderRegistry.register
class PDFLoader(BaseLoader):
    """

        Responsiable For:
            - file validation
            - Opening PDF
            - Delegating Extraction
            - Building Document object
    """

    @classmethod
    def name(cls) -> str:
        return ".pdf"


    def validate(self) -> None:

        if not self.file_path.exists():
            raise FileNotFoundError(
                f"File not found: {self.file_path} "
            )
        
        if not self.file_path.is_file():
            raise ValueError(
                f"Not a valid File: {self.file_path} "
            )
        
        if self.file_path.suffix.lower() not in self.supports():
            raise UnsupportedFileTypeError(
                f"Unsupported file type: {self.file_path.suffix} "
            )
    

    def load(self) -> Document:

        self.validate()
        
        logger.info("Loading PDF: %s", self.file_path.name)

        try:
            with fitz.open(self.file_path) as pdf:

                text = TextExtractor.extract(pdf)

                metadata = MetadataGenerator.generate(
                    document=pdf,
                    file_path=self.file_path,
                    text=text
                )

                document = Document(
                    document_id = str(uuid4()),
                    source = str(self.file_path),
                    file_name= self.file_path.name,
                    file_path= self.file_path, 
                    content= text,
                    metadata= metadata,
                )

                logger.info(
                    "successfully loaded '%s' (%d pages)",
                    self.file_path.name,
                    metadata.page_count
                )

                return document
            
        except Exception as ex:
            logger.exception(
                "failed tp load PDF: %s",
                self.file_path.name
            )
            raise DocumentLoadingError(
                f"Unable to load PDF: {self.file_path} "
             ) from ex
       