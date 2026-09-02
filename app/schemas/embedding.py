from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from numpy.typing import NDArray
import numpy as np

class Embedding(BaseModel):
    """
        Embedding generate from chunks.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        arbitrary_types_allowed=True,
    )

    embedding_id: str = Field(
        description="Unique embedding identifier."
    )

    chunk_id: str = Field(
        description="Associated chunk identifier."
    )

    model_name: str = Field(
        description="Embedding model used"
    )

    dimension: int = Field(
        gt=0

    )

    vector: NDArray[np.float32] = Field(
        description="use NDarray for better performance , convert to list[float] when serialization required."
    )