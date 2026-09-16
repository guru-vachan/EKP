from __future__ import annotations

from app.schemas.context import Context
from app.schemas.guardrail_result import GuardrailViolation
from app.schemas.llm_response import LLMResponse

from app.guardrail.interfaces.base_guardrail import BaseGuardrail
from app.guardrail.guardrail_registry import GuardrailRegistry


@GuardrailRegistry.register
class ResponseGuardrail(BaseGuardrail):

    @classmethod
    def name(cls) -> str:
        return "response"
    

    def validate(self,
                 response: LLMResponse,
                 context: Context
                ) -> GuardrailViolation | None:
        
        content = response.content.strip()


        if not content:
            return GuardrailViolation(
                guardrail=self.name(),
                reason="LLM returned an empty response."
            )
        
        return None