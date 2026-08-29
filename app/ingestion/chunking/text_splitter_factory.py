from __future__ import annotations

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    TextSplitter,
    TokenTextSplitter
)
from app.config.config import ChunkingConfig

class TextSplitterFactory:
    """
        using factory, only one file knows about LangChain otherwise need to import in every chunker.
        example:
            RecursiveChunker -> TextSplitterFactory -> LangChain
        
        adding more splitter is straightforward.
            TextSplitterFactory.recursive()
            TextSplitterFactory.token()
            TextSplitterFactory.semantic()
    """

    _MATCH = {
        "recursive": lambda config: RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        ),

        "token": lambda config: TokenTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
        ),
    }

    @classmethod
    def create(cls, strategy: str, config: ChunkingConfig) -> TextSplitter:
        """
            create a Generic Splitter.
        """

        creator = cls._MATCH.get(strategy)

        if creator is None:
            raise ValueError(f"Unsupported chunking strategy: {strategy}")
        
        return creator(config)
