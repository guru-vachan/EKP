from __future__ import annotations

from pathlib import Path 

import pytest

from tests.builders.pipeline_builder import (
    build_ingestion_pipeline,
    build_retrieval_pipeline,
    build_generation_pipeline,
)

@pytest.mark.integration
def test_generation_pipeline(
    tmp_path: Path,
) -> None:
    
    pdf_path = Path("data/raw/sample.pdf")

    assert pdf_path.exists()

    ingestion = build_ingestion_pipeline(storage_dir=tmp_path)

    generation_pipeline = build_generation_pipeline(storage_dir=tmp_path)

    ingestion_result = ingestion.ingest(pdf_path)

    assert ingestion_result.document_id
    assert ingestion_result.chunk_created>0
    assert ingestion_result.embedded_created>0


    response = generation_pipeline.generate(
        "what are Working Hours and Attendance"
    )

    assert response.query_id

    assert response.answer.strip()
    assert response.provider == "gemini"
    assert response.model_name

    assert response.usage.input_tokens >= 0
    assert response.usage.output_tokens > 0
    assert response.usage.total_tokens > 0

    