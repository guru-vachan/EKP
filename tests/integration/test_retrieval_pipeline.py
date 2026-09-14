from __future__ import annotations

from pathlib import Path 

import pytest

from tests.builders.pipeline_builder import (
    build_ingestion_pipeline,
    build_retrieval_pipeline,
)

@pytest.mark.integration
def test_pdf_to_faiss_end_to_end(
    tmp_path: Path,
) -> None:
    
    pdf_path = Path("data/raw/sample.pdf")

    ingestion = build_ingestion_pipeline(storage_dir=tmp_path)

    retrieval = build_retrieval_pipeline(storage_dir=tmp_path)

    ingestion.ingest(pdf_path)

    results = retrieval.retrieve(
        "what are Working Hours and Attendance"
    )

    assert results

    assert len(results) > 0

    assert results[0].chunk is not None

    assert results[0].score > 0

    assert (results[0].retrieval_method == "hybrid" )