from __future__ import annotations

import pickle
from pathlib import Path
from rank_bm25 import BM25Okapi

from app.config.config import LexicalSearchConfig
from app.retrieval.lexical_search.interfaces.base_lexical_search import BaseLexicalSearch
from app.retrieval.lexical_search.lexical_search_registry import LexicalSearchRegistry

from app.schemas.query import Query
from app.schemas.search_result import SearchResult
from app.schemas.chunk import Chunk
from app.schemas.FilterCriteria import FilterCriteria

@LexicalSearchRegistry.register
class BM25Search(BaseLexicalSearch):

    def __init__(self, config: LexicalSearchConfig) -> None:
        super().__init__(config)
        self._bm25: BM25Okapi | None = None
        self._chunks: list[Chunk] = []
    
    @classmethod
    def name(cls) -> str:
        return "bm25"
    

    def build(self, chunks: list[Chunk]) -> None:
        
        self._chunks = chunks
   
        corpus = [
            chunk.content.split()
            for chunk in chunks
        ]
        print("corpus")
        print(corpus)
        self._bm25 = BM25Okapi(corpus)


    def search(self, 
             query: Query,
             filters: FilterCriteria,
            ) -> list[SearchResult]:
        
        if self._bm25 is None:
            raise RuntimeError(
                "BM25 index has not been built."
            )
        
        tokenized_query = query.query.split()

        scores = self._bm25.get_scores(
            tokenized_query
        )

        ranked = sorted(
            zip(self._chunks, scores),
            key=lambda item: item[1],
            reverse=True,
        )

        results: list[SearchResult] = []

        rank = 1

        for chunk, score in ranked:

            if rank > self._config.top_k:
                break

            # Todo
            # Metadata filter implement later
            #

            results.append(
                SearchResult(
                    chunk_id=chunk.chunk_id,
                    chunk=chunk,
                    rank=rank,
                    score=float(score),
                    vector_store="bm25",
                    retrieval_method="lexical"
                )
            )

            rank += 1
        
        return results
    

    def persist(self, directory: Path) -> None:
        directory.mkdir(parents=True, exist_ok=True)

        with open(directory / "bm25.pkl", "wb") as file:
            pickle.dump(
                {
                    "bm25": self._bm25,
                    "chunks": self._chunks,
                },
                file,
            )


    def load(self, directory: Path) -> None:
        with open(directory / "bm25.pkl", "rb") as file:
            data = pickle.load(file)

        self._bm25 = data["bm25"]
        self._chunks = data["chunks"]