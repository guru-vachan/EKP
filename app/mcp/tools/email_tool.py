from __future__ import annotations

from typing import Any

from app.agents.tool.email_tool import EmailTool

from app.schemas.tool import ToolInput

class EmailMCPTool:

    def __init__(self, email_tool: EmailTool) -> None:

        self._email_tool = email_tool
    

    def execute(
            self,
            recipient: str,
            subject: str,
            body: str,
    ) -> dict[str, Any]:
        
        result = self._email_tool.execute(
            ToolInput(
                arguments={
                    "recipient": recipient,
                    "subject": subject,
                    "body": body,

                }
            )
        )

        return {
            "success": result.success,
            "data": result.data,
            "error": result.error,
        }



