from app.ingestion.ingestion_manager import IngestionManager
from app.ingestion.chunking.chunking_manager import ChunkingManager
from app.config.config import ChunkingConfig
from app.ingestion.chunking.recursive_chunker import RecursiveChunker


document = IngestionManager.ingest("data/raw/sample.pdf")

print("Document ID:", document.document_id)
print("Content length:", len(document.content or ""))
print("Content meta:", (document.metadata or ""))

config = ChunkingConfig(
    chunk_size=1000,
    chunk_overlap=200,
    strategy = "recursive"
)

manager = ChunkingManager(config)

chunks = manager.chunk(
    document=document,
    strategy="recursive",
)

print("Number of chunks:", len(chunks))

for chunk in chunks:
    print("\n--- Chunk", chunk.chunk_index, "---")
    print(chunk.content[:200])