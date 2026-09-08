from __future__ import annotations

import logging
from uuid import uuid4

from app.config.config import QueryConfig
from app.retrieval.query_processing.query_utils import (
    normalize_query,
)
from app.retrieval.query_processing.validators import (
    validate_query,
)
from app.schemas.query import Query

logger = logging.getLogger(__name__)

class QueryProcessor:
    """
        Orchestrates query processing.

        Responsibilities:
            - Normalize query
            - validate query
            - Return Query schema
    """

    def __init__(self, config: QueryConfig) -> None:

        self._config = config
    

    def process(self, query: str) -> Query:

        logger.info("processing Query...")

        original_query = query

        processed_query = normalize_query(
            query=query,
            preserve_case=self._config.preserve_case
        )
        logger.info("Query processed successfully.")

        return Query(
            query_id=str(uuid4()),
            original_query=original_query,
            query=processed_query
        )