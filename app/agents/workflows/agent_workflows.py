from __future__ import annotations

from app.agents.nodes.action_node import ActionNode
from app.agents.nodes.knowledge_node import KnowledgeNode
from app.agents.nodes.planner_node import PlannerNode

from app.schemas.agent_state import AgentState
from app.schemas.execution_plan import AgentIntent

from langgraph.graph import END, START, StateGraph

class AgenWorkflow:
    
    """
        Builds and executes the EKIP agent workflow.
    """

    def __init__(
            self,
            planner_node: PlannerNode,
            knowledge_node: KnowledgeNode,
            action_node: ActionNode,
    ) -> None:
        
        self._planner_node = planner_node
        self._knowledge_node = knowledge_node
        self._action_node = action_node

        self._graph = self._build_graph()


    def _build_graph(self):

        builder = StateGraph(AgentState)

        builder.add_node(
            "planner",
            self._planner_node,
        )

        builder.add_node(
            "knowledge",
            self._knowledge_node,
        )

        builder.add_node(
            "action",
            self._action_node,
        )

        builder.add_edge(
            START,
            "planner"
        )

        builder.add_conditional_edges(
            "planner",
            self._route_intent,
            {
                AgentIntent.KNOWLEDGE: "knowledge",
                AgentIntent.ACTION: "action"
            },
        )

        builder.add_edge(
            "knowledge",
            END
        )

        builder.add_edge(
            "action",
            END
        )

        return builder.compile()


    @staticmethod
    def _route_intent(
            state: AgentState
    ) -> AgentIntent:
        
        if state.plan is None:
            raise ValueError(
                "Execution plan is missing"
            )
        
        return state.plan.intent
    
    async def invoke(
            self,
            user_request: str,
    ) -> AgentState:
        """
            Execute the agent workflow.
        """

        initial_state = AgentState(
            user_request=user_request,
        )

        result = self._graph.ainvoke(
            initial_state
        )

        return AgentState.model_validate(
            result
        )
    
        

