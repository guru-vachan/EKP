from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import AgentIntent

class Planstep (BaseModel):
    """
        Represents one executable step in an agent plan.
    """
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )
    step_id: int = Field(ge=1)

    action: str = Field( 
        min_length=1,
    )

    description: str = Field(
        min_length=1,
    )

    tool_name: str | None = None

class ExecutionPlan(BaseModel):

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )
    intent: AgentIntent

    steps: list[Planstep] = Field(
        default_factory=list
    )