from __future__ import annotations

from abc import ABC, abstractmethod

from app.schemas.tool import ToolInput, ToolResult

class BaseTool(ABC):

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        raise NotImplementedError
    

    @abstractmethod
    def execute(
            self,
            tool_input: ToolInput
    ) -> ToolResult:
        
        raise NotImplementedError