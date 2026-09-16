from __future__ import annotations

from app.schemas.context import Context
from app.schemas.guardrail_result import GuardrailViolation, GuardrailResult
from app.schemas.llm_response import LLMResponse

from app.guardrail.interfaces.base_guardrail import BaseGuardrail
from app.guardrail.guardrail_registry import GuardrailRegistry

class GuardrailManager:

    def __init__(
            self, 
            guardrail_names: tuple[str, ...],
    ) -> None:
        
        self._guardrails: tuple[BaseGuardrail, ...] = tuple(
            GuardrailRegistry.get(name)()
            for name in guardrail_names
        )

    
    def validate(
            self, 
            response: LLMResponse,
            context: Context,
    ) -> GuardrailResult:
        
        """
            Execute all configured guardrails.
        """
        violations: list[GuardrailViolation] = []

        for guardrail in self._guardrails:
            violation = guardrail.validate(
                response=response,
                context=context,
            )

            if violation is not None:
                violations.append(violation)
        

        return GuardrailResult(
            passed=not violations,
            violation=violations
        )