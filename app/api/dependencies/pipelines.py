from fastapi import Request
from app.bootstrap.application_builder import (
    ApplicationContainer
)
from app.generation.generation_pipeline import GenerationPipeline
from app.ingestion.ingestion_pipeline import IngestionPipeline


def get_container(
        request: Request,
)-> ApplicationContainer:
    return request.app.state.container


def get_ingestion_pipeline(
        request: Request,
) -> IngestionPipeline:
    return get_container(request).ingestion_pipeline


def get_generation_pipeline(
        request: Request,
)-> GenerationPipeline:
    return get_container (request).generation_pipeline