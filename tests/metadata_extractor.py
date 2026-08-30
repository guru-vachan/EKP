import fitz
from pathlib import Path

from app.ingestion.extractors.metadata_extractor import MetaDataExtractor

"""
to run test cases:
    python -m pytest tests/metadata_extractor.py -v -s
"""

def test_extract_pdf_metadata():
    pdf_path = Path("data/raw/sample.pdf")

    with fitz.open(pdf_path) as document:

        document.set_metadata({
            "title": "Employee Handbook 2026",
            "author": "ABC Technologies",
            "subject": "Company policies and employee guidelines",
            "creator": "EKP Sample PDF Generator",
            "producer": "EKP Test Suite",
        })
        

        metadata = MetaDataExtractor.extract(
            document,
            pdf_path,
        )

        print(metadata.title )

        assert metadata.title == "Employee Handbook 2026"
        assert metadata.author == "ABC Technologies"
        assert metadata.subject == "Company policies and employee guidelines"
        assert metadata.creator == "EKP Sample PDF Generator"
        assert metadata.producer == "EKP Test Suite"

        assert metadata.page_count == document.page_count
        assert metadata.file_size > 0