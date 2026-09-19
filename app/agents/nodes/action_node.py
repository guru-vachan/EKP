from __future__ import annotations

from app.agents.tool_router.tool_router import ToolRouter
from app.agents.tool_router.mcp_tool_router import MCPToolRouter
from app.schemas.agent_state import AgentState
from app.schemas.tool import ToolInput

class ActionNode:

    def __init__(
            self,
            tool_router: MCPToolRouter
    ) -> None:
        
        self._tool_router = MCPToolRouter

    
    async def __call__(
            self, 
            state: AgentState,
            ) -> dict[str, object]:
        
        if state.plan is None:
            return {
                "error": "Execution plan is missing."
            }
        
        tool_results = dict(state.tool_results)

        try:

            for step in state.plan.steps:

                if not step.tool_name:
                    continue

            #    tool_input = ToolInput(
            #        arguments=step.arguments
            #    )

            #    result = self._tool_router.execute( 
            #        step=step,
            #        tool_input=tool_input,
            #    )

                result = await self._tool_router.execute(
                    step=step
                )

                tool_results[str(step.step_id)] = (
                    result.model_dump()
                )

                if not result.success:
                    return {
                        "tool_results": tool_results, 
                        "current_step": step.step_id,
                        "error": result.error,
                    }
            
            return {
                "tool_results": tool_results,
                "current_step": len(state.plan.steps),
                "final_response": (
                    "Requested action completed successfully."
                ),
                "error": None,
            }
        except Exception as exc:

            return {
                "tool_results": tool_results,
                "error": str(exc),
            }
