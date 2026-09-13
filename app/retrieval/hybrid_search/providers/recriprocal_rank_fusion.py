from __future__ import annotations

from app.retrieval.hybrid_search.interfaces.base_hybrid_search import BaseHybridSearch
from app.retrieval.hybrid_search.hybrid_search_registry import HybridSearchRegistry
from app.schemas.search_result import SearchResult
from app.config.config import HybridSearchConfig


@HybridSearchRegistry.register
class RecriprocalRankFusion(BaseHybridSearch):
    """
        Reference:
            score(d) = sum(1 / k + rank(d))
    """

    def __init__(self, config: HybridSearchConfig) -> None:
        super().__init__(config)
    
    @classmethod
    def name(cls) -> str:
        return "rrf"
    

    def _update_score(self,
                      results: list[SearchResult],
                      scores: dict[str, float],
                      documents: dict[str, SearchResult],
                      ) -> None:
        
        for result in results:

            score = 1.0 / (
                self._config.rrf_k + result.rank
            )
            scores[result.chunk_id] = (
                scores.get(result.chunk_id, 0.0) + score
            )
            documents[result.chunk_id] = result

    def fuse(self, 
             vector_results: list[SearchResult],
             lexical_result: list[SearchResult],
            ) -> list[SearchResult]:
        
        scores: dict[str, float] = {}
        documents: dict[str, SearchResult] = {}

        self._update_score(
            vector_results,
            scores,
            documents
        )

        self._update_score(
            lexical_result,
            scores,
            documents
        )

        results: list[SearchResult] = []

        for rank, (chunk_id, score) in enumerate(
            sorted(
                scores.items(),
                key=lambda item: item[1],
                reverse=True,
            ),
            start=1
        ):
            result = documents[chunk_id]

            results.append(
                result.model_copy(
                    update={
                        "score": score,
                        "rank": rank,
                        "retrieval_method": "hybrid"
                    }
                )
            )
        
        return results