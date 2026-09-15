from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

class Prompt(BaseModel):
    
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    system_instruction: str

    user_query: str

    context: str