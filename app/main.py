from __future__ import annotations

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from app.api.middleware.request_context import (
    RequestContextMiddleware
)
from app.api.routes.health import router as health_router
from app.api.routes.query import router as query_router
from app.api.routes.ingestion import router as ingest_router
from app.bootstrap.application_builder import build_application
import app.config.config as settings

@asynccontextmanager
async def lifespan ( app: FastAPI,)  -> AsyncIterator [None]:
    """
        Manage EKIP application lifecycle.
    """
    app.state.container = build_application( settings )

    yield

    # Provider cleanup will be added here when resources
    # requiring explicit shutdown are introduced.

def create_app()-> FastAPI:

    app = FastAPI(
        title="Enterprise Knowledge Intelligence Platform", 
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        RequestContextMiddleware
    )

    app.include_router(
        health_router
    )
    app.include_router(
        ingest_router
    )
    app.include_router(
        query_router
    )

    return app

app = create_app()
