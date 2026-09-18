from __future__ import annotations

from app.agents.planner.interfaces.base_planner import BasePlanner
from app.schemas.agent_state import AgentState

class PlannerNode:
    """
        Langgraph adapter for the agent planner.
    """

    def __init__(
            self,
            planner: BasePlanner
    ) -> None:
        
        self._planner = planner

    
    def __call__(self, 
                 state: AgentState,
                ) -> dict[str, object]:
        
        plan = self._planner.plan(state)

        return {
            "plan": plan,
            "current_step": 0,
            "error": None
        }