from __future__ import annotations

from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.execution_plan import ExecutionPlan

class AgentState(BaseModel):
    """
    state carried throughout the agent workflow.
    This will later become the state passed between LangGraph nodes.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    request_id: str = Field(
        default_factory=lambda: str(uuid4()),
    )

    user_request: str = Field(
        min_length=1,
    )

    plan: ExecutionPlan | None = None

    current_step: int = Field(
        default=0,
        ge=0,
    )

    tool_results: dict[str, Any] = Field(
        default_factory=dict
    )

    final_response: str | None = None

    error: str | None = None