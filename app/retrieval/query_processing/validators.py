from __future__ import annotations

from app.config.config import QueryConfig
from app.core.exceptions import QueryValidationError

def validate_not_empty(query: str) -> None:
    """
        Validate that the query is not empty
    """
    if not query.strip():
        raise QueryValidationError(
            "query cannot be empty."
        )
    

def validate_max_length(query: str, config: QueryConfig) -> None:
    """
        Validate maximum query length.
    """
    if len(query) > config.max_query_length:
        raise QueryValidationError(
            f"query exceed maximum length."
            f"({config.max_query_length})."
        )

def validate_min_length(query: str, config: QueryConfig) -> None:
    """
        Validate maximum query length.
    """
    if len(query.strip()) < config.min_query_length:
        raise QueryValidationError(
            f"query minimum length."
            f"({config.min_query_length})."
        )


def validate_query(query: str, config: QueryConfig) -> None:
    """
        Execute all query Validation.
    """
    validate_not_empty(query)

    validate_max_length(query, config)

    validate_min_length(query, config)