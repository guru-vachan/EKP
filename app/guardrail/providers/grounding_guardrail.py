from __future__ import annotations

from app.schemas.context import Context
from app.schemas.guardrail_result import GuardrailViolation
from app.schemas.llm_response import LLMResponse

from app.guardrail.interfaces.base_guardrail import BaseGuardrail
from app.guardrail.guardrail_registry import GuardrailRegistry

import re


@GuardrailRegistry.register
class GroundingGuardrail(BaseGuardrail):

    _SOURCE_PATTERN = re.compile(
        r"\[Source:\s*([^\]]+)\]",
        re.IGNORECASE,
    )

    @classmethod
    def name(cls) -> str:
        return "grounding"
    

    def validate(self,
                 response: LLMResponse,
                 context: Context
                ) -> GuardrailViolation | None:
        
        if not context.items:
            return None
        
        cited_chunk_ids = set(
            self._SOURCE_PATTERN.findall(
                response.content
            )
        )

        if not cited_chunk_ids:
            return GuardrailViolation (
                guardrail=self.name(),
                reason="Response contains no source citations.",
            )
        
        allowed_chunk_ids = (
            item.chunk_id
            for item in context.items
        )
        invalid_citations = (
            cited_chunk_ids - set(allowed_chunk_ids)
        )
        if invalid_citations:
            return GuardrailViolation(
                guardrail=self.name(),
                reason=(
                    "Response references unknown source IDs: "
                    f"{sorted(invalid_citations)}"
                ),
            )
        
        return None