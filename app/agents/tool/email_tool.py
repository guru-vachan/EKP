from __future__ import annotations

import smtplib
from email.message import EmailMessage

from pydantic import ValidationError

from app.agents.tool.tool_registry import ToolRegistry
from app.agents.tool.interfaces.base_tool import BaseTool

from app.schemas.tool import ToolInput, ToolResult
from app.schemas.email import EmailRequest, EmailResult

from app.config.config import EmailConfig

@ToolRegistry.register
class EmailTool (BaseTool):
    """
        Send email through an SMTP provider.
    """

    def __init__(
            self,
            config: EmailConfig,
    ) -> None:
        self._config = config

    @classmethod    
    def name(cls) -> str:
        return "email"
    

    def execute(
            self,
            tool_input: ToolInput
    ) -> ToolResult:
        
        try:
            request = EmailRequest.model_validate(
                tool_input.arguments
            )
        
        except ValidationError as exc:
            return ToolResult(
                tool_name=self.name(),
                success=False,
                error=str(exc)
            )
        
        message= EmailMessage()
        message["From"] = self._config.sender 
        message[ "To"] = str(request.recipient)
        message["Subject"] = request.subject 
        message.set_content (request.body)

        try:

            with smtplib.SMTP(
                self._config.host,
                self._config.port,
                timeout=self._config.timeout_seconds,
                ) as smtp:

                if self._config.use_tls:
                    smtp.starttls()
                
                if self._config.username:
                    smtp.login(
                        self._config.username,
                        self._config.password,
                    )
                
                smtp.send_message(message)
        
        except (smtplib.SMTPException, OSError) as exc:

            return ToolResult(
                tool_name=self.name(),
                success=False,
                error=str(exc)
            )
        
        result = EmailResult(
            recipient=request.recipient,
            message_id=message.get("Message-ID")
        )
        return ToolResult(
                tool_name=self.name(),
                success=True,
                data=result.model_dump(
                    mode="json"
                )
            )