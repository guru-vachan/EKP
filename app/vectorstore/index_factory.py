from __future__ import annotations

import faiss

from app.config.config import VectorStoreConfig

class IndexFactory:
    """
        factory for crating faiss index.
    """

    @staticmethod
    def create(config: VectorStoreConfig) -> faiss.Index:

        match config.index_type.lower():

            case "flat_l2":
                return faiss.IndexFlatL2(
                    config.dimension
                )
            
            case "flat_ip":
                return faiss.IndexFlatIP(
                    config.dimension
                )
            
            case "hnsw":
                return faiss.IndexHNSWFlat(
                    config.dimension,
                    config.hnsw_m
                )
            
            case _:
                raise ValueError(
                    f"unsupported index type"
                )
