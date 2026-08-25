from __future__ import annotations

import fitz  # PyMuPDF

from app.schemas.pageContent import PageContent


class TextExtractor:
    """
    
        This class responsiable only for text extraction.
        It does not perform text cleaing, metadata extraction,
        or document construction.
    """

    @staticmethod
    def extract(document: fitz.Document) -> str:
        """
            Extract text feom all pages of a pdf.

            Return: complete document text as a single string.
        """
        pages: list[PageContent] = []

        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text")

            if text:
                pages.append(
                    PageContent(
                        page_number = page_number,
                        text = text.strip()
                    )
                )

        return pages