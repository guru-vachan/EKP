from __future__ import annotations


from app.config.config import LLMConfig
from app.llm.llm_registry import LLMRegistry
from app.llm.interfaces.base_llm import BaseLLM
from app.schemas.llm_response import LLMResponse
from app.schemas.prompt import Prompt

from app.core.enums import LLMProvider


class LLMManager:

    def __init__(self, config: LLMConfig) -> None:

        self._config = config

        provider_cls = LLMRegistry.get(
            config.provider
        )
        print("provider_cls ================ ")
        print(provider_cls)
        if config.provider == LLMProvider.GEMINI:
            self._provider: BaseLLM = provider_cls(
                config.gemini
            )
    

    def generate(self, prompt: Prompt) -> LLMResponse:

        return self._provider.generate( prompt )
    

    @property
    def provider_name(self) -> str:
        """
            return active llm provider name
        """
        return self._provider.name()
