from __future__ import annotations

import json

from app.agents.planner.interfaces.base_planner import BasePlanner
from app.llm.llm_manager import LLMManager
from app.schemas.agent_state import AgentState
from app.schemas.execution_plan import ExecutionPlan
from app.schemas.prompt import Prompt

class LLMPlanner (BasePlanner):
    """
        Creates structured execution plans using the configured LLM
    """

    _SYSTEM_INSTRUCTION = """
You are the planning Component of an enterprise A agent.
classify the request as:
- knowledge: information can be answered using enterprise knowledge. 
- action: one or more external tools must be executed.

Return ONLY valid JSON matching this structure:
{
    "intent": "knowledge | action",
    "steps": [
    {
        "step_id": 1,
        "action": "action_name",
        "description": "what this step should accomplish", 
        "tool_name": "tool_name or null",
        "arguments": {
            "recipient": "user@example.com",
            "subject": "subject",
            "body": "Message"
        }
    }
  ]
}

Available capabilities:
- enterprise_knowledge: retrieve and answer terprise knowledge
- email: perform email-related actions

Rules:
- Create the minimum number of steps required.
- Do not execute any action.
- Do not invent unavailable tools.
- Knowledge-only requests must use enterprise_knowledge.
""".strip()
    
    def __init_(
            self,
            llm_manager: LLMManager,
    ) -> None:
        self._llm =llm_manager
    
    def plan(
            self,
            state: AgentState,
    ) -> ExecutionPlan:
        
        prompt = Prompt (
            system_instruction=self._SYSTEM_INSTRUCTION,
            user_query=state.user_request,
            context=""
        )

        response = self._llm.generate(prompt)

        payload = self._parse_json(
            response.content
        )

        return ExecutionPlan.model_validate( payload )
    

    @staticmethod
    def _parse_json(
        content: str,
        )-> dict[str, object]:
        """
            parse structured planner output.
        """
        normalized = content.strip()

        # Tolerate markdown fences occasionally returned by models.

        if normalized.startswith("```"):
            lines = normalized.splitlines()

            if lines:
                lines = lines [1:]
            
            if lines and lines[-1].strip() == "```" :
                lines = lines [:-1]
            
            normalized = "\n".join(lines).strip()

            try:
                payload = json.loads(normalized)

            except json.JSONDecodeError as exc:

                raise ValueError("Planner returned invalid JSON.") from exc
            
            if not isinstance(payload, dict):
                raise ValueError(
                    "Planner response must be a JSON object"
                )
            
            return payload