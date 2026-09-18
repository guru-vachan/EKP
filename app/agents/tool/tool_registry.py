from __future__ import annotations

from app.core.registry import Registry
from app.agents.tool.interfaces.base_tool import BaseTool


ToolRegistry = Registry[BaseTool]()

