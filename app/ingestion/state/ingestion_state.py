from __future__ import annotations

from app.ingestion.state.ingestion_status import IngestionStatus

class IngestionState:
    """ 
        Tracks ingestion status by ingestion key.
    """

    def __init__(self) -> None:
        self._state: dict[str, IngestionStatus] = {}

    def get(self, ingestion_key: str,) -> IngestionStatus | None:

        return self._state.get(ingestion_key)
    
     def mark(self, ingestion_key: str, status: IngestionStatus) -> None:

        self._state[ingestion_key] = status