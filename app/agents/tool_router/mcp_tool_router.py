from __future__ import annotations

from typing import Any

from app.mcp.client.mcp_client import MCPClient

from app.schemas.tool import ToolResult
from app.schemas.execution_plan import Planstep

class MCPToolRouter:
    """
        Routes planned tool calls through an MCP client.
        
        Discovery is performed through MCP before invocation so only 
        capabilities exposed by the connected MCP server can execute
    """

    def __init__(
            self,
            client: MCPClient,
    ) -> None:
        
        self._client = client
        self._available_tools: set[str] = set()

    
    async def discover(self) -> set[str]:
        """
            Discover and cache tools exposed by the MCP server.
        """
        result = await self._client.list_tools()

        self._available_tools = {
            tool.name
            for tool in result.tools
        }

        return self._available_tools.copy()
    
    async def execute( 
            self,
            step: Planstep,
    ) -> ToolResult:
        """
            Invoke the tool selected by the planner.
        """
        
        if not step.tool_name:
            return ToolResult(
                tool_name="unknown",
                success=False,
                error="Plan step does not specify a tool.",
            )
        
        if not self._available_tools:
            await self.discover()
        
        if step.tool_name not in self._available_tools:
            return ToolResult(
                tool_name=step. tool_name,
                success=False,
                error=(
                    f"MCP tool '{step.tool_name} "
                    "is not available."
                ),
            )
        
        try:
            result = await self._client.call_tool(
                tool_name=step.tool_name,
                arguments=step.arguments,
            )
             
            if result.is_error:
                return ToolResult(
                    tool_name=step.tool_name,
                    success=False,
                    error=self._extract_text(result.content),
                )
            
            return ToolResult(
                tool_name=step.tool_name,
                success=True,
                data={
                    "content": self._extract_content(
                        result.content
                    )
                },
            )
        except Exception as exc:

            return ToolResult(
                tool_name=step.tool_name,
                success=False,
                error=str(exc),
            )
    

    @staticmethod
    def _extract_text(
            content: list [Any],
    )-> str:
        return " ".join(
            str(getattr(item, "text", item))
            for item in content
        )
    
    @staticmethod
    def _extract_content(
            content: list [Any],
    ) -> list [Any]:
        return [
            getattr(item, "text", item)
            for item in content
        ]
