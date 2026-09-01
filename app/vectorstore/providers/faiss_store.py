from __future__ import annotations

import json
from pathlib import Path

import faiss
import numpy as np

from app.config.config import VectorStoreConfig
from app.schemas.embedding import Embedding
from app.schemas.search_result import SearchResult
from app.vectorstore.interface.base_vectorstore import BaseVectorStore
from app.vectorstore.vectorstore_registry import VectorStoreRegistry
from app.vectorstore.index_factory import IndexFactory

@VectorStoreRegistry.register
class FAISSStore(BaseVectorStore):

    def __init__(self, config: VectorStoreConfig) -> None:

        self._config = config

        self._index = IndexFactory.create(
            config
        )
        self._mapping: dict[int, str] = {}

    
    @classmethod
    def name(cls) -> str:
        return "faiss"
    
    def add(self, embeddings: list[Embedding]) -> None:

        if not embeddings:
            return
        
        vectors = np.vstack(
            [e.vector for e in embeddings]
        ).astype(np.float32)

        start = self._index.ntotal

        self._index.add(vectors)

        for offset, embedding in enumerate(embeddings):
            self._mapping[start + offset] = embedding.chunk_id

    
    def search(self, query_vector: np.ndarray, top_k: int) -> list[SearchResult]:

        distances, indicies = self._index.search(
            query_vector.reshape(1, -1),
            top_k,
        )

        results: list[SearchResult] = []

        for rank, (distance, idx) in enumerate(
            zip(distances[0], indicies[0]),
            start=1
        ):
            
            if idx == -1:
                continue

            results.append(
                SearchResult(
                    chunk_id=self._mapping[idx],
                    score=float(distance),
                    rank=rank,
                    vector_store=self.name()
                )
            )

        return results
    
    def persist(self, directory: Path) -> None:

        """
            ToDo:
                index_to_chunk_id.json will replace with sqlite. Json take some time to load after lots of records.
        """

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        faiss.write_index(
            self._index,
            str(directory / "faiss.index"),
        )

        with open(
            directory / "index_to_chunk_id.json",
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                self._mapping,
                file,
                indent=4, 
            )
        
    
    def load(self, directory: Path) -> None:

        self._index = faiss.read_index(
            str(directory / "faiss.index")
        )

        with open(
            directory / "index_to_chunk_id.json",
            "r",
            encoding="utf-8",
        ) as file:
            
            mapping = json.load(file)

        self._mapping = {
            int(k): v
            for k, v in mapping.items() 
        }