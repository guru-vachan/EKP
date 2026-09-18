from __future__ import annotations

from pathlib import Path

import pytest

from app.agents.tool.interfaces.base_tool import BaseTool
from app.schemas.tool import ToolInput, ToolResult
from tests.builders.pipeline_builder import (
    build_agent_workflow,
    build_ingestion_pipeline,
)


class FakeEmailTool (BaseTool):
    """
        Test double that prevents real email delivery.
    """

    @classmethod
    def name(cls) -> str:
        return "email"
    

    def execute(self,
                tool_input: ToolInput,
    )-> ToolResult:
        
        return ToolResult(
            tool_name=self.name(),
            success=True,
            data={
                "recipient": tool_input.arguments.get("recipient"), 
                "subject": tool_input. arguments.get("subject"),
            },
        )
    

@pytest.mark.integration
def test_agent_knowledge_workflow ( tmp_path: Path,) -> None:

    pdf_path = Path("data/raw/sample.pdf")

    ingestion = build_ingestion_pipeline(storage_dir=tmp_path)

    ingestion.ingest(pdf_path)

    workflow = build_agent_workflow(
        storage_dir=tmp_path, 
        tools=[FakeEmailTool()],
    )

    result = workflow.invoke(
        "what are Working Hours and Attendance?"
    )

    assert result.plan is not None 
    assert result.error is None 
    assert result.final_response 
    assert result.plan.intent.value == "knowledge"


@pytest.mark.integration
def test_agent_email_workflow ( tmp_path: Path,) -> None:


    workflow = build_agent_workflow(
        storage_dir=tmp_path, 
        tools=[FakeEmailTool()],
    )

    result = workflow.invoke(
        "Send an email to test@example.com "
        "with subject Project Update' saying"
        "'The project is progressing well'"
    )

    assert result.plan is not None
    assert result.plan.intent.value == "action"
    assert result.error is None
    assert result.tool_results

    email_steps = [
        step
        for step in result.plan.steps
        if step.tool_name == "email"
    ]

    assert email_steps
    email_step = email_steps[0]

    assert(
        email_step.arguments["recipient"] 
        == "test@example.com"
    )

    assert(
        email_step.arguments["subject"] 
        == "Project Update"
    )

    tool_result = result.tool_results[
        str(email_step.step_id)
    ]

    assert tool_result["success"] is True
    assert tool_result["tool_name"] == "email"

    assert (
        tool_result["data"]["recipient"] ==
        "test@example.com"
    )

