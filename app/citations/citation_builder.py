from __future__ import annotations

import re
from uuid import uuid4

from app.schemas.context import Context
from app.schemas.citation import Citation
from app.schemas.llm_response import LLMResponse


class CitationBuilder:

    _SOURCE_PATTERN = re.compile(
        r"\[Source:\s*([^\]]+)\]",
        re.IGNORECASE,
    )

    def build(self, response: LLMResponse, context: Context,) -> list[Citation]:
        """
            Resolve LLM-generated source references against the exact context supplied during generation.
        """

        source_ids = self._extract_source_ids(
            response.content
        )
        if not source_ids:
            return []
        
        context_by_chunk_id = {
            item.chunk_id: item
            for item in context.items
        }

        citations: list[Citation] = []
        seen: set[str] = set()

        for chunk_id in source_ids:
            if chunk_id in seen:
                continue

            item = context_by_chunk_id.get(chunk_id)
            
            # Never accept a citation that was not part
            # of the generation context.
            if item is None:
                continue

            metadata = item.metadata

            citations.append(
                Citation(
                    citation_id=str(uuid4()),
                    chunk_id=item.chunk_id,
                    document_id=item.document_id,
                    source=self._get_source(metadata),
                    page_number=self._get_page_number(metadata),
                    rank=item.rank,
                )
            )
            seen.add(chunk_id)

        return citations
    

    @classmethod
    def _extract_source_ids(cls, content: str,)-> list[str]:
        """
            Extract source chunk IDs while preserving citation order.
        """
        return [
            source_id.strip()
            for source_id in cls._SOURCE_PATTERN.findall (content)
            if source_id.strip()
        ]
    
    @staticmethod
    def _get_source(metadata: dict[str, object],) -> str | None:

        """
            Resolve the best available human-readable source.
        """
        for key in (
            "source",
            "file_name",
            "title",
        ):
            value = metadata.get(key)

            if value is not None:
                normalized = str(value).strip()

                if normalized:
                    return normalized
                
        
        return None
    

    @staticmethod
    def _get_page_number( metadata: dict[str, object],)-> int | None:

        value = metadata.get("page_number")

        if value is None:
            return None
        
        try:
            page_number = int(value)
        except(TypeError, ValueError):
            return None
        
        return page_number if page_number > 0 else None


