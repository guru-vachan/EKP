from __future__ import annotations

import sqlite3
from pathlib import Path

from app.schemas.chunk import Chunk
from app.schemas.metadata import Metadata
from app.chunkstore.intefaces.base_chunk_store import BaseChunkStore
from app.chunkstore.chunk_store_registry import ChunkStoreRegistry

from app.config.config import ChunkStoreConfig

@ChunkStoreRegistry.register
class SQLiteChunkStore(BaseChunkStore):

    def __init__(self, config: ChunkStoreConfig) -> None:
        
        super().__init__(config)

        # Create a SQLite connection.
        self._connection = sqlite3.connect(
            config.storage_directory
        )
        # Initialize the database schema.
        self._initialize()
        self._connection.row_factory = sqlite3.Row

    
    @classmethod
    def name(cls) -> str:
        return "sqlite"
    

    def _initialize(self) -> None:
        """
        Create the chunks table if it does not exist.
        """

        cursor = self._connection.cursor()
        query = """
            CREATE TABLE IF NOT EXISTS chunks (
                chunk_id TEXT PRIMARY KEY,
                document_id TEXT NOT NULL,
                chunk_index INTEGER NOT NULL,
                content TEXT NOT NULL
            );
        """

        cursor.execute(query)

        self._connection.commit()



    def add(self, chunks: list[Chunk]) -> None:
        """
        Insert multiple chunks into the database.

        Args:
            chunks: List of Chunk objects to store.
        """
        if not chunks:
            return

        cursor = self._connection.cursor()

        query = """
            INSERT OR REPLACE INTO chunks (
                chunk_id,
                document_id,
                chunk_index,
                content
            )
            VALUES (?, ?, ?, ?);
        """

        values = [
            (
                chunk.chunk_id,
                chunk.document_id,
                chunk.chunk_index,
                chunk.content,
            )
            for chunk in chunks
        ]

        cursor.executemany(query, values)
        self._connection.commit()

    
    def get(self, chunk_id: str) -> Chunk | None:
        """
        Retrieve a single chunk by its ID.

        Args:
            chunk_id: Unique chunk identifier.

        Returns:
            Chunk object if found, otherwise None.
        """
        query = """
            SELECT
                chunk_id,
                document_id,
                chunk_index,
                content
            FROM chunks
            WHERE chunk_id = ?;
        """
        cursor = self._connection.cursor()

        row = cursor.execute(
            query,
            (chunk_id,),
        ).fetchone()

        if row is None:
            return None

        return Chunk.model_validate(
            {
                "chunk_id": row[0],
                "document_id": row[1],
                "chunk_index": row[2],
                "content": row[3],
            }
        )
    

    def get_many(self, chunk_ids: list[str]) -> list[Chunk]:

        if not chunk_ids:
            return []
        
        # Remove duplicates while preserving input order.
        unique_ids = list(dict.fromkeys(chunk_ids))

        placeholders = ", ".join(
            "?" for _ in unique_ids
        )

        query = f"""
            SELECT
                chunk_id,
                document_id,
                chunk_index,
                content
            FROM chunks
            WHERE chunk_id IN ({placeholders});
        """

        cursor = self._connection.cursor()

        rows = cursor.execute(
            query,
            unique_ids,
        ).fetchall()

        # Convert rows into a lookup dictionary.
        chunks_by_id = {
            row["chunk_id"]: self._row_to_chunk(row)
            for row in rows
        }

        # Preserve the order requested by the caller.
        return [
            chunks_by_id[chunk_id]
            for chunk_id in unique_ids
            if chunk_id in chunks_by_id
        ]

    @staticmethod
    def _row_to_chunk(row: sqlite3.Row) -> Chunk:
        """
        Convert a SQLite row into a Chunk object.
        """
        return Chunk(
            chunk_id=row["chunk_id"],
            document_id=row["document_id"],
            chunk_index=row["chunk_index"],
            content=row["content"],
            metadata=Metadata(),
            character_count=len(row["content"]),
        )
    

    def exists(self, chunk_id: str) -> bool:

        """
        Check whether a chunk exists in the database.

        Args:
            chunk_id: Unique chunk identifier.

        Returns:
            True if the chunk exists, otherwise False.
        """
        query = """
            SELECT 1
            FROM chunks
            WHERE chunk_id = ?
            LIMIT 1;
        """

        cursor = self._connection.cursor()

        row = cursor.execute(
            query,
            (chunk_id,),
        ).fetchone()
        
        return row is not None
    

    def delete(self, document_id: str) -> None:
        
        cursor = self._connection.cursor()

        query = """
            DELETE FROM chunks
            WHERE document_id = ?;
        """

        cursor.execute(
                query,
                (document_id,),
            )
