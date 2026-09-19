from __future__ import annotations

from typing import Any

from mcp.server import MCPServer

from app.agents.tool.email_tool import EmailTool
from app.bootstrap.application_builder import build_application

import app.config.config as settings

from app.mcp.tools.email_tool import EmailMCPTool
from app.mcp.tools.knowlwdge_tool import KnowledgeMCPTool

# core part: create MCP server

mcp = MCPServer(
    "EKIP"
)

container = build_application(settings=settings)

knowlwdge_adapter = KnowledgeMCPTool(
    generation_pipeline=container.generation_pipeline
)

email_adapter = EmailMCPTool(
    email_tool=EmailTool(
        settings.EmailConfig
    )
)

# @mcp.tool() => tool expose and registration 

@mcp.tool()
def knowlwdge_query(
        query: str
) -> dict[str, Any]:
    
    return knowlwdge_adapter.execute(
        query=query
    )


@mcp.tool()
def send_email(
        recipient: str,
        subject: str,
        body: str,
) -> dict[str, Any]:
    
    return email_adapter.execute(
        recipient=recipient,
        subject=subject,
        body=body,
    )


def main() -> None:
    # MCP transport server
    mcp.run()


if __name__ == "__main__":
    main()

