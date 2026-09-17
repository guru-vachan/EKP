from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, UploadFile
from pydantic import BaseModel, ConfigDict, Field
from starlette.concurrency import run_in_threadpool

from app.schemas.ingestion_result import IngestionResult
from app.ingestion.ingestion_pipeline import IngestionPipeline
from app.api.dependencies.pipelines import get_ingestion_pipeline


router = APIRouter(
    prefix="/api/v1/ingest",
    tags=["ingestion"],
)


@router.post("", response_model=FinalResponse)
async def ingest_document(file: UploadFile,
                          pipeline: IngestionPipeline = Depends(
                              get_ingestion_pipeline
                          ),
                
) -> IngestionResult:
    

    suffix = Path(file.filename or "").suffix.lower()

    with tempfile.NamedTemporaryFile(
        suffix=suffix,
        delete=False,
    ) as temp_file:
        temp_path = Path(temp_file.name)
        shutil.copyfileobj(file.file, temp_file)

    try:

        return await run_in_threadpool(
            pipeline.ingest,
            temp_path,
        )
    finally:
        temp_path.unlink(missing_ok=True)
        await file.close()
