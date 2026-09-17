from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from starlette.concurrency import run_in_threadpool

from app.schemas.final_response import FinalResponse
from app.generation.generation_pipeline import GenerationPipeline
from app.api.dependencies.pipelines import get_generation_pipeline

class QueryRequest(BaseModel):

    model_config = ConfigDict(
        # Don't allow fields that aren't defined in the schema.
        extra="forbid"
    )
    query: str

router = APIRouter(
    prefix="/api/v1/query",
    tags=["query"],
)

@router.post("", response_model=FinalResponse)
async def query(request: QueryRequest,
                pipeline: GenerationPipeline = Depends(
                    get_generation_pipeline
                ),
) -> FinalResponse:
    
    return await run_in_threadpool (
        pipeline.generate,
        request.query,
    )