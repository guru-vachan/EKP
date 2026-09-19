from __future__ import annotations

from typing import Any

from app.generation.generation_pipeline import GenerationPipeline

class KnowledgeMCPTool:

    def __init__(self, generation_pipeline: GenerationPipeline) -> None:

        self._generation_pipeline = generation_pipeline
    
    def execute(
            self,
            query: str
    ) -> dict[str, Any]:
        
        response = self._generation_pipeline.generate(query)

        return {
            "answer": response.answer,
            "citation": [
               citation.model_dump(mode="json")
                for citation in response.citation
            ]
        }