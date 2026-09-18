from __future__ import annotations

from app.generation.generation_pipeline import GenerationPipeline 
from app.schemas.agent_state import AgentState

class KnowledgeNode:
    """
        Handle knowledge oriented agent request
    """

    def __init__(
            self,
            generation_pipeline: GenerationPipeline
    ) -> None:
        
        self._generation = generation_pipeline

    
    def __call__(
            self, 
            state: AgentState,
            ) -> dict[str, object]:
        
        try:

            response = self._generation.generate(
                state.user_request
            )

            return {
                "final_response": response.answer,
                "error": None
            }
        except Exception as exc:

            return {
                "final_response": None,
                "error": str(exc)
            }

        