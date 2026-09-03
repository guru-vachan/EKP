from enum import Enum

class IngestionStatus(str, Enum):
    PROCESSING = "processing"
    COMMITTED = "committed"
    FAILED ="failed"