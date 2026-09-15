from __future__ import annotations

from abc import ABC, abstractmethod

from app.schemas.llm_response import LLMResponse
from app.schemas.prompt import Prompt

class BaseLLM(ABC):

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        """
            Return provider name

            eg:
                - gemini
                - openai
        """

        raise NotImplementedError
    

    @abstractmethod
    def generate(self, prompt: Prompt) -> LLMResponse:

        raise NotImplementedError