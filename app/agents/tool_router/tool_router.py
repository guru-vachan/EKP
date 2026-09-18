from __future__ import annotations

from app.agents.tool.interfaces.base_tool import BaseTool

from app.schemas.tool import ToolInput, ToolResult
from app.schemas.execution_plan import Planstep

class ToolRouter:
    """
        Resolves and executes the tool requested by a plan step
    """

    def __init__(
            self,
            tools: list[BaseTool],
    ) -> None:
        self._tools = dict[str, BaseTool] = {
            tool.name().lower(): tool
            for tool in tools
        }


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
        
        tool = self._tools.get(
                step.tool_name.lower()
            )
        
        if tool is None:
            return ToolResult(
                tool_name=step.tool_name,
                success=False,
                error=(
                    f"plan step '{step.tool_name}'"
                    "does not specify a tool."
                ),
            )
        
        try:
            
            return tool.execute(
                tool_input
            )
        except Exception as ex:
            return ToolResult(
                tool_name=step.tool_name,
                success=False,
                error=str(ex),
            )