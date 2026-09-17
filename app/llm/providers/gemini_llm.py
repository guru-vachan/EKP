from __future__ import annotations

import logging

from google import genai
from google.genai import types

from app.config.config import GeminiConfig
from app.llm.llm_registry import LLMRegistry
from app.llm.interfaces.base_llm import BaseLLM
from app.schemas.llm_response import LLMResponse, LLMUsage
from app.schemas.prompt import Prompt

logger = logging.getLogger(__name__)


@LLMRegistry.register
class GeminiLLM(BaseLLM):

    def __init__(self, config: GeminiConfig) -> None:

        self._config = config

        print("=====================")
        print(config.api_key)
        self._client = genai.Client(
            api_key=config.api_key
        )

    @classmethod
    def name(cls) -> str:
        return "gemini"
    

    def generate(self, prompt: Prompt) -> LLMResponse:

        logger.info("Generating response using Gemini model '%s'.", 
                    self._config.model_name,)
        
        try:
            response = self._client.models.generate_content(
                model=self._config.model_name,
                contents=self._build_user_content (prompt),
                config=types.GenerateContentConfig(
                    system_instruction=prompt.system_instruction,
                    temperature=self._config.temperature,
                    max_output_tokens = self._config.max_output_tokens,
                ),
            )

            content = response.text or ""

            usage = self._extract_usage(response)

            finish_reason = self._extract_finish_reason(response)

            logger.info("Gemini generation complete. "
                        "input_tokens-%d output_tokens=%d",
                        usage.input_tokens,
                        usage.output_tokens,
            )

            return LLMResponse(
                content=content.strip(),
                model_name=self._config.model_name,
                provider=self.name(),
                usage=usage,
                finish_reason=finish_reason,
            )
        
        except Exception:
            logger.exception( "Gemini generation failed for model '%s'.",
                             self._config.model_name,)
            
            raise

    @staticmethod
    def _build_user_content( prompt: Prompt,) -> str:
        """
            Build Gemini user content while keeping 
            the system instruction separate from untrusted query/context.
        """
        return (
            "Retrieved context: \n"
            f" {prompt.context}\n\n" 
            "User question: \n"
            f"{prompt.user_query}"
        )
    
    @staticmethod
    def _extract_usage(response: object,)-> LLMUsage:
        """
            Normalize Gemini token usage into EKIP's domain schema.
        """

        metadata = getattr(
            response,
            "usage_metadata",
            None,
            )
        
        if metadata is None:
            return LLMUsage()
        
        input_tokens = (
            getattr(metadata, "prompt_token", 0)
            or 0
        )

        output_tokens = (
            getattr(metadata, "candidates_token_count", 0)
            or 0
        )

        total_tokens = (
            getattr(metadata, "total_token_count", 0)
            or input_tokens + output_tokens
        )

        return LLMUsage(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
        )
    
    @staticmethod
    def _extract_finish_reason( response: object,) -> str | None:

        """
            Extract the finish reason without leaking Gemini-specific 
            response objects outside the provider.
        """

        candidates = getattr(
             response,
            "candidates",
            None,
            )
        
        if candidates is None:
            return None
        
        finish_resons = getattr(
                candidates[0], 
                "finish_resons", 
                None
            )
        
        if finish_resons is None:
            return None
        
        return getattr(
            finish_resons,
            "name",
            str(finish_resons)
        )