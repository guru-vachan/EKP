from __future__ import annotations

import logging

from app.config.config import ContextConfig
from app.schemas.context import Context, ContextItem
from app.schemas.search_result import SearchResult

logger = logging.getLogger(__name__)

class ContextBuilder:
    """
    Responsibilities:
        - preserve retrival ranking.
        - Remove context token budget.
        - Enforce context token budget.
        - preserve metadata for cition.
        - produce structed and text context.
    """

    def __init__(self, config: ContextConfig) -> None:

        self._config = config

    def build(self, results: list[SearchResult]) -> Context:
        """
        Build context from retrival result.
        """

        if not results:
            return Context(
                items=[],
                text="",
                total_chunks=0,
                estimated_tokens=0
            )

        ranked_results = sorted(
            results,
            key=lambda result: result.rank
        )

        items: list[ContextItem] = []
        context_blocks: list[str] = []

        seen_chunk_ids: set[str] = set()
        used_tokens = 0

        for result in ranked_results:

            chunk = result.chunk

            if chunk is None:
                continue

            if chunk.chunk_id in seen_chunk_ids:
                continue

            content = chunk.content.strip()

            if content is None:
                continue

            estimated_tokens = self._estimated_tokens(
                content
            )

            if (
                used_tokens + estimated_tokens 
                > self._config.max_tokens
            ):
                continue

            item = ContextItem(
                chunk_id=chunk.chunk_id,
                document_id=chunk.document_id,
                content=content,
                rank=result.rank,
                score=result.score,
                metadata=chunk.metadata.model_dump()
            )

            items.append(item)
            context_blocks.append(
                self._format_context_block(item)
            )

            seen_chunk_ids.add(chunk.chunk_id)
            used_tokens += estimated_tokens

            if len(items) >= self._config.max_chunks:
                break

        logger.info(
            "context build: chunk: %d estimated token: %d",
            len(items),
            used_tokens
        )

        return Context(
            items=items,
            text="\n\n".join(context_blocks),
            total_chunks=len(items),
            estimated_tokens=used_tokens
        )
    
    @staticmethod
    def _estimated_tokens(text: str)-> int:

        return max(1, (len(text) + 3) // 4)
    

    @staticmethod
    def _format_context_block(item: ContextItem) -> str:

        return (
            f"[Source: {item.chunk_id}]\n"
            f"{item.content}"
        )

        