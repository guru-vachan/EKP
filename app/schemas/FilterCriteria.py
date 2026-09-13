from pydantic import BaseModel

from app.config.config import MetadataFilterConfig


class FilterCriteria(BaseModel):
    filters: list[MetadataFilterConfig]