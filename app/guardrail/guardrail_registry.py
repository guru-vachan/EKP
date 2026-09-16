from __future__ import annotations

from app.core.registry import Registry
from app.guardrail.interfaces.base_guardrail import BaseGuardrail

GuardrailRegistry = Registry[BaseGuardrail]()