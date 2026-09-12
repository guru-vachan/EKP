from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

class Query(BaseModel):

    model_config = ConfigDict(
        frozen=True,
        extra="forbid"
    )

    query_id : str

    query: str = Field(
        min_length=1,
        description="processed user query"
    )

    original_query: str = Field(
        min_length=1,
        description="original user input"
    )

    rewritten: bool = False