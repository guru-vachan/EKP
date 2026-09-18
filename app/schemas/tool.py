from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

class ToolInput(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    arguments: dict[str, Any] = Field(
        default_factory=dict
    )


class ToolResult(BaseModel):

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )
    tool_name: str 

    success: bool

    data: dict[str, Any] = Field(
        default_factory=dict
    )

    error: str | None = None

