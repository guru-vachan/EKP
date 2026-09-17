from __future__ import annotations

import re

_WHITESPACE_PATTERN = re.compile(r"\s+")


def normalize_whitespace(query: str) -> str:
    """
        replace multiple whitespace characters with a single space.
    """

    return _WHITESPACE_PATTERN.sub(
        " ",
        query,
    ).strip()

def remove_control_character(query: str) -> str:
    """
        remove non printable control characters.
    """
    print("+++++++++++++++++++++++++")
    print(type(query), query)
    print("+++++++++++++++++++++++++")

    return "".join(
        character
        for character in query
        if character.isprintable()
    )

def normalize_query(
        query: str,
        *,
        preserve_case: bool = True
    ) -> str:
    

    query = remove_control_character(query)

    query = normalize_whitespace(query)

    return query