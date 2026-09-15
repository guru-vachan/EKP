from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

class LLMUsage(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    input_tokens: int

    output_tokens: int

    total_tokens: int


class LLMResponse(BaseModel):

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    content: str

    model_name: str

    provider: str

    usage: str

    finish_reason: str | None = None
