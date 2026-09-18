from __future__ import annotations

from abc import ABC, abstractmethod

from app.schemas.agent_state import AgentState
from app.schemas.execution_plan import ExecutionPlan

class BasePlanner(ABC):

    def plan(
            self,
            state: AgentState
    ) -> ExecutionPlan:
        """
            create a execution plan for  the current state.
        """
        raise NotImplementedError