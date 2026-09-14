from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Optional

from app.core.enums import (
    ChunkingStrategy,
    EmbeddingProvider,
    VectorStoreProvider,
    IndexType,
    FilterOperator,
    ChunkStoreProvider,
)



def get_file_size(file_path: Path) -> int:
    """
        return file size in Bytes.
    """

    return file_path.stat().st_size


def get_file_extension(file_path: Path) -> str:
     
     return file_path.suffix.lower()


def get_file_name(file_path: Path) -> str:
     
    return file_path.name


def calculate_checksum(
    file_path: Path,
    algoritham: str = "sha256",
    buffer_size: int =  1024 * 1024,
) -> str:
    
    # hasher = hashlib.new(algoritham)
    hasher = hashlib.sha256()

    with file_path.open("rb") as file:

        while chunk := file.read(buffer_size):
            hasher.update(chunk)
        
    return hasher.hexdigest()


def build_ingestion_key(
        checksum: str, 
        chunking_strategy: ChunkingStrategy,
        chunk_size: int,
        chunk_overlap: int,
        embedding_model: str,) -> str:
    
    value = (
        f"{checksum}:"
        f"{chunking_strategy}:"
        f"{chunk_size}:"
        f"{chunk_overlap}:"
        f"{embedding_model}:"
    )

    return hashlib.sha256(
        value.encode("utf-8")
    ).hexdigest()


def normalize_string(value: Optional[str]) -> Optional[str]:

    if value is None:
        return None
    
    value = value.strip()

    return value or None


def estimate_word_count(text: str) -> int:

    return len(text.split())


def estimate_character_count(text: str) -> int:

    return len(text)