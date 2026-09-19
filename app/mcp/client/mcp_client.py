from __future__ import annotations

from typing import Any
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import CallToolResult, ListToolsResult

class MCPClient:
    """
        generic MCP client for tool discovery and invocation.
    """

    """
        contains information about how to start your MCP server.
        eg: 
            server_parameters = StdioServerParameters(
                    command="python",
                    args=["app/mcp/server.py"],
                )
    """
    def __init__(
            self,
            server_parameters: StdioServerParameters,
            )-> None:
        
        self._server_parameters = server_parameters
        self._session: ClientSession | None = None
        self._exit_stack = AsyncExitStack()

    async def connect(self) -> None:
        """
            connect to MCP server and initialize the session
        """

        read_stream, write_stream = (
            await self._exit_stack.enter_async_context(
                stdio_client(self._server_parameters)
            )
        )

        self._session = (
            await self._exit_stack.enter_async_context(
                ClientSession(
                    read_stream,
                    write_stream,
                )
            )
        )

        await self._session.initialize()

    # tool discovery
    async def list_tools(self) -> ListToolsResult:
        """
            Discover tools exposed by MCP server.
        """

        session = self._require_session()

        return await session.list_tools()
    

    async def call_tool(
            self,
            tool_name: str,
            arguments: dict[str, Any],
    ) -> CallToolResult:
        
        session = self._require_session()

        return await session.call_tool(
            name=tool_name,
            arguments=arguments
        )
    
    async def close(self) -> None:

        await self._exit_stack.aclose()
        self._session = None

    
    async def __aenter__(self) -> "MCPClient":
        await self.connect()
        return self
    
    async def __aexit__(
            self,
            exc_type: object,
            exc_value: object,
            traceback: object

        ) -> None:
        await self.close()

    
    def _require_session(self) -> ClientSession:

        if self._session is None:
            raise RuntimeError(
                "MCP client is not connected."
            )
        
        return  self._session 