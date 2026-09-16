from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

class GuardrailViolation(BaseModel):

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    guardrail: str
    reason: str


class GuardrailResult(BaseModel):

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )
    passed: bool

    violation: list[GuardrailViolation] = Field(
        default_factory=list
    )
