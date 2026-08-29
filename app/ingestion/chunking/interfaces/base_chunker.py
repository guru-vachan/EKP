from __future__ import annotations

from abc import ABC, abstractmethod

from app.schemas.document import Document
from app.schemas.chunk import Chunk


class BaseChunker(ABC):
    """
        Abstruct base class for all chunking strategies.

        Every chunker must convert a Document into list of chunks
    """

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        """
        
            return chunker name, eg: recursive, semantic, token 
        """
        raise NotImplementedError


    @abstractmethod
    def split(self, document: Document) -> list[Chunk]:
        """
            split a document into chunks.
        """
        raise NotImplementedError