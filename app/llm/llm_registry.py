from __future__ import annotations

from app.core.registry import Registry
from app.llm.interfaces.base_llm import BaseLLM


LLMRegistry = Registry[BaseLLM]()