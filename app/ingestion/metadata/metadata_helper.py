from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Optional

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
) -> str:
    
    hasher = hashlib.new(algoritham)

    with file_path.open("rb") as file:

        while chunk := file.read(8192):
            hasher.update(chunk)
        
    return hasher.hexdigest()

def normalize_string(value: Optional[str]) -> Optional[str]:

    if value is None:
        return None
    
    value = value.strip()

    return value or None

def estimate_word_count(text: str) -> int:

    return len(text.split())

def estimate_character_count(text: str) -> int:

    return len(text)