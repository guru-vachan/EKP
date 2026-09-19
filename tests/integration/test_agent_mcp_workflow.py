from __future__ import annotations

import pytest

from app.agents.nodes.action_node import ActionNode
from app.agents.tool_router.mcp_tool_router import MCPToolRouter
from app.schemas.execution_plan import Planstep

class FakeTool:
    def __init__(self, name: str) -> None:
        self.name = name


class FakeListToolsResult:
    def __init__(self) -> None:
        self.tools = [
            FakeTool("knowledge_query"), 
            FakeTool ("send_email"),
        ]
        

class FakeContent:
    def __init__(self, text: str) -> None:
        self.text = text

class FakeCallToolResult:
    def __init__(
            self,
            text: str,
            is_error: bool = False
    ) -> None:
        self.content = [FakeContent(text)]
        self.is_error = is_error

class FakeMCPClient:
    """
        Test double for MCP discovery and invocation.
    """
    def __init__(self) -> None:
        self.called_tools: list[
            tuple[str, dict[str, object]]
        ] = []
    
    async def list_tools (self) -> FakeListToolsResult: 
        return FakeListToolsResult()
    
    async def call_tool(
            self,
            tool_name: str,
            arguments: dict[str, object],
    ) -> FakeCallToolResult:
        self.called_tools.append(
            (tool_name, arguments)
        )

        return FakeCallToolResult(
            text="Tool executed successfully."
        )
    

async def test_mcp_tool_discovery_and_invocation() -> None:

    client = FakeMCPClient()
    router = MCPToolRouter(
        client=client, #type: ignore [arg-type]
    )

    # ------------------------
    # Discover
    # ------------------------
    tools = await router.discover()
    assert tools == {
        "knowledge_query",
        "send_email",
    }

    # ------------------------
    # Invoke
    # ------------------------
    step = Planstep(
        step_id=1,
        action="send_email",
        description="Send project update email.",
        tool_name="send_email",
        arguments={
            "recipient": "test@example.com", 
            "subject": "Project Update",
            "body": "Project is progressing well.",
        },
    )

    result = await router.execute(step)

    # ------------------------
    # Validate
    # ------------------------


    assert result.success is True
    assert result.tool_name == "send_email"

    assert client.called_tools == [
        (
            "send_email",
            {
                "recipient": "test@example.com", 
                "subject": "Project Update",
                "body": "Project is progressing well.",
            },
        )
    ]