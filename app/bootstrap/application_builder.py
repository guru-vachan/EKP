from __future__ import annotations

from dataclasses import dataclass

# Provider imports execute registry decorators.
import app.chunkstore.providers.sqlite_chunk_store # noqa: F401 
import app.embeddings.providers.bge_embedding # noqa: F401 
import app.guardrail.providers. grounding_guardrail # noqa: F401 
import app.guardrail.providers.response_guardrail # noga: F401 
import app.ingestion.loaders.pdf_loader # noqa: F401
import app.llm.providers 
import app.retrieval.hybrid_search.providers
import app.retrieval.lexical_search.providers
import app.retrieval.metadata_filtering.providers
import app.retrieval.query_rewriting.providers
import app.vectorstore.providers

from app.chunkstore.chunk_store_manager import ChunkStoreManager 
from app.citations.citation_builder import CitationBuilder
import app.config.config as Settings
from app.embeddings.embedding_manager import EmbeddingManager 
from app.generation.generation_pipeline import GenerationPipeline 
from app.guardrail.guardrail_manager import GuardrailManager 
from app.ingestion.chunking.chunking_manager import ChunkingManager 
from app.ingestion.ingestion_manager import IngestionManager 
from app.ingestion. ingestion_pipeline import IngestionPipeline 
from app.llm.llm_manager import LLMManager 
from app.llm.prompt_builder import PromptBuilder 
from app.retrieval.context_builder.context_builder import ContextBuilder
from app.retrieval.hybrid_search.hybrid_search_manager import HybridSearchManager
from app.retrieval.lexical_search.lexical_search_manager import LexicalSearchManager
from app.retrieval.metadata_filtering.metadata_filter_manager import MetadataFilterManager
from app.retrieval.query_processing.query_processor import QueryProcessor
from app.retrieval.query_rewriting.query_rewriting_manager import QueryRewriterManager
from app.vectorstore.vectorstore_manager import VectorStoreManager
from app.ingestion.state.ingestion_state import IngestionState

from app.core.enums import (
    VectorStoreProvider,
    EmbeddingProvider,
    IndexType,
    ChunkingStrategy,
    ChunkStoreProvider,
    LLMProvider
)

from app.retrieval.retrieval_pipeline import RetrievalPipeline

from pathlib import Path 


@dataclass(frozen=True)
class ApplicationContainer:

    ingestion_pipeline: IngestionPipeline 
    generation_pipeline: GenerationPipeline

def build_application( settings: Settings, ) -> ApplicationContainer:

    embedding_config = settings.EmbeddingConfig(
        provider=EmbeddingProvider.BGE,
        model_name="BAAI/bge-small-en-v1.5",
        device="cpu",
        batch_size=16,
        normalize_embeddings=True,
    )

    vector_store_config = settings.VectorStoreConfig(
        provider=VectorStoreProvider.FAISS,
        dimension=384,
        index_type=IndexType.FLAT_IP,
        top_k=3,
        storage_directory=Path("data/vector_store"),
    )

    chunk_store_config = settings.ChunkStoreConfig(
        storage_directory= Path("data/chunk_store")
    )

    query_config = settings.QueryConfig()

    chunking_config = settings.ChunkingConfig(
        strategy=ChunkingStrategy.RECURSIVE,
        chunk_size=500,
        chunk_overlap=100,
    )

    query_rewrite_config = settings.QueryRewriteConfig(
        provider="identity",
        model_name="gemini-2.5-flash",
        temperature=0.0,
        max_tokens=512,
        system_prompt="Rewrite the user's query for better retrieval.",
    )

    metadata_filter_config = settings.MetadataFilterConfig(
        provider="exact_match",
        field="source",
        operator="eq",
        value="sample2.pdf",
    )

    lexical_search_config = settings.LexicalSearchConfig(
        provider="bm25",
    )

    hybrid_search_config = settings.HybridSearchConfig(
        provider="rrf",
    )

    context_config = settings.ContextConfig()

    llm_config = settings.LLMConfig(
        provider=LLMProvider.GEMINI,
        gemini=Settings.GeminiConfig(
            model_name="gemini-2.5-flash",
        ),
    )

    # -------------------------
    # Managers
    # -------------------------

    embedding_manager = EmbeddingManager(
        embedding_config
    )

    vector_store = VectorStoreManager(
        vector_store_config
    )

    vector_store.initialize()

    chunk_store = ChunkStoreManager(
        chunk_store_config
    )

    query_processor = QueryProcessor(
        query_config
    )

    # -------------------------
    # Retrieval Pipeline
    # -------------------------

    retrieval_pipeline = RetrievalPipeline(
        query_processor=query_processor,
        query_rewriter=QueryRewriterManager(
            query_rewrite_config
        ),
        metadata_filter=MetadataFilterManager(
            metadata_filter_config
        ),
        embedding=embedding_manager,
        vector_store=vector_store,
        chunk_store=chunk_store,
        lexical_search=LexicalSearchManager(
            lexical_search_config
        ),
        hybrid_search=HybridSearchManager(
            hybrid_search_config
        ),
    )

    # -------------------------
    # Ingestion Pipeline
    # -------------------------

    ingestion_pipeline = IngestionPipeline(
        ingestion_manager=IngestionManager(),

        chunking_manager=ChunkingManager(
            chunking_config
        ),

        embedding_manager=embedding_manager,

        vector_store_manager=vector_store,

        ingestion_state=IngestionState(),

        chunking_config=chunking_config,
        embedding_config=embedding_config,
        vector_store_config=vector_store_config,

        chunkstore_manager=chunk_store,

        lexical_search_manager=LexicalSearchManager(
            lexical_search_config
        ),
    )

    # -------------------------
    # Generation Pipeline
    # -------------------------

    generation_pipeline = GenerationPipeline(
        query_processor=query_processor,

        retrieval_pipeline=retrieval_pipeline,

        context_builder=ContextBuilder(
            context_config
        ),

        prompt_builder=PromptBuilder(),

        llm_manager=LLMManager(
            llm_config
        ),

        guardrail_manager=GuardrailManager(
            guardrail_names=(
                "response",
                "grounding",
            )
        ),

        citation_builder=CitationBuilder(),
    )

    return ApplicationContainer(
        ingestion_pipeline=ingestion_pipeline,
        generation_pipeline=generation_pipeline
    )