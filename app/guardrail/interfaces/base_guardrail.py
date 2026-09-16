from __future__ import annotations

from abc import ABC, abstractmethod

from app.schemas.context import Context
from app.schemas.guardrail_result import GuardrailViolation
from app.schemas.llm_response import LLMResponse

class BaseGuardrail(ABC):

    @classmethod
    @abstractmethod
    def name(cls) -> str:

        raise NotImplementedError
    
    def validate(self,
                 response: LLMResponse,
                 context: Context
                ) -> GuardrailViolation | None:
        
        raise NotImplementedError