from __future__ import annotations

from app.agents.tool.tool_registry import ToolRegistry

from app.schemas.tool import ToolInput, ToolResult
from app.schemas.execution_plan import Planstep

class ToolRouter:
    """
        Resolves and executes the tool requested by a plan step
    """

    def execute(
            self,
            step: Planstep,
            tool_input: ToolInput,
    ) -> ToolResult:
        
        if not step.tool_name:
            return ToolResult(
                tool_name="unknown",
                success=False,
                error=(
                    f"plan step '{step.action}'"
                    "does not specify a tool."
                ),
            )
        
        try:
            tool_cls = ToolRegistry.get(
                step.tool_name
            )

            tool = tool_cls

            return tool.execute(
                tool_input
            )
        except Exception as ex:
            return ToolResult(
                tool_name=step.tool_name,
                success=False,
                error=str(ex),
            )