from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.citation import Citation
from app.schemas.guardrail_result import  GuardrailResult
from app.schemas.llm_response import LLMUsage, LLMResponse

class FinalResponse(BaseModel):

    query_id : str

    answer : str

    citation: list[Citation] = []

    model_name: str

    provider: str

    usage: LLMUsage

    guardrail_result: GuardrailResult

