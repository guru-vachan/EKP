from __future__ import annotations

from pathlib import Path

import app.embeddings.providers
import app.ingestion.chunking
import app.ingestion.loaders
import app.vectorstore.providers
import app.chunkstore.providers
import app.retrieval.lexical_search.providers
import app.retrieval.hybrid_search.providers
import app.retrieval.metadata_filtering.providers
import app.retrieval.query_rewriting.providers
import app.guardrail.providers
import app.llm.providers

from app.core.enums import (
    ChunkingStrategy,
    EmbeddingProvider,
    VectorStoreProvider,
    IndexType,
    FilterOperator,
    ChunkStoreProvider,
    LLMProvider,
)

from tests.builders.test_environment import TestEnvironment

from app.config.config import (
    ChunkingConfig,
    EmbeddingConfig,
    VectorStoreConfig,
    QueryConfig,
    QueryRewriteConfig,
    MetadataFilterConfig,
    ChunkStoreConfig,
    LexicalSearchConfig,
    HybridSearchConfig,
    ContextConfig,
    LLMConfig,
    GeminiConfig
)

from app.embeddings.embedding_manager import EmbeddingManager
from app.vectorstore.vectorstore_manager import VectorStoreManager
from app.ingestion.ingestion_manager import IngestionManager
from app.ingestion.chunking.chunking_manager import ChunkingManager
from app.retrieval.hybrid_search.hybrid_search_manager import HybridSearchManager
from app.retrieval.lexical_search.lexical_search_manager import LexicalSearchManager
from app.retrieval.metadata_filtering.metadata_filter_manager import MetadataFilterManager
from app.retrieval.query_processing.query_processor import QueryProcessor
from app.retrieval.query_rewriting.query_rewriting_manager import QueryRewriterManager
from app.vectorstore.vectorstore_manager import VectorStoreManager
from app.chunkstore.chunk_store_manager import ChunkStoreManager
from app.ingestion.state.ingestion_state import IngestionState
from app.retrieval.context_builder.context_builder import ContextBuilder
from app.citations.citation_builder import CitationBuilder
from app.guardrail.guardrail_manager import GuardrailManager
from app.llm.llm_manager import LLMManager
from app.llm.prompt_builder import PromptBuilder

from app.ingestion.ingestion_pipeline import IngestionPipeline
from app.retrieval.retrieval_pipeline import RetrievalPipeline
from app.generation.generation_pipeline import GenerationPipeline

from app.retrieval.lexical_search.lexical_search_registry import LexicalSearchRegistry



def build_test_environment(storage_dir: Path) -> TestEnvironment: 
    """ 
        Build a complete test environment using the supplied storage directory. 
    """ 

    return TestEnvironment( 
        query_config=QueryConfig(), 

        query_rewrite_config=QueryRewriteConfig(
            provider="identity",
            model_name="gemini-2.5-flash",
            temperature=0.0,
            max_tokens=512,
            system_prompt="Rewrite the user's query for better retrieval.",
        ), 

        metadata_filter_config=MetadataFilterConfig(
            provider = "exact_match",
            field="source",
            operator="eq",
            value="sample2.pdf",
        ),

        chunking_config=ChunkingConfig(
            strategy=ChunkingStrategy.RECURSIVE,
            chunk_size=500,
            chunk_overlap=100
        ), 
        embedding_config=EmbeddingConfig(
            provider=EmbeddingProvider.BGE.value, 
            model_name="BAAI/bge-small-en-v1.5", 
            device="cpu", 
            batch_size=16, 
            normalize_embeddings=True, 
        ), 

        vector_store_config=VectorStoreConfig(
            provider=VectorStoreProvider.FAISS.value, 
            dimension=384, 
            index_type=IndexType.FLAT_IP.value, 
            top_k=3, 
            storage_directory= storage_dir / "vector_store",
            ),

        chunk_store_config=ChunkStoreConfig( 
            storage_directory=storage_dir / "chunk_store"
            ), 
        lexical_search_config=LexicalSearchConfig(
            provider="bm25",
        ), 
        hybrid_search_config=HybridSearchConfig(
            provider="rrf",
        ),
        context_config=ContextConfig(),
        llm_config=LLMConfig(
            provider=LLMProvider.GEMINI,
            gemini=GeminiConfig(
                model_name="gemini-2.5-flash"
            )
        ),  

        )


def build_ingestion_pipeline(storage_dir: Path) -> IngestionPipeline:

    env = build_test_environment(storage_dir)

    return IngestionPipeline(
        ingestion_manager = IngestionManager(),
        chunking_manager = ChunkingManager(env.chunking_config),
        embedding_manager = EmbeddingManager(env.embedding_config), 
        vector_store_manager = VectorStoreManager(env.vector_store_config), 
        ingestion_state= IngestionState(),
        chunking_config= env.chunking_config,
        embedding_config= env.embedding_config,
        vector_store_config= env.vector_store_config,
        chunkstore_manager= ChunkStoreManager(env.chunk_store_config),
        lexical_search_manager= LexicalSearchManager(env.lexical_search_config),
    )


def build_retrieval_pipeline(storage_dir: Path) -> RetrievalPipeline:

    env = build_test_environment(storage_dir)

    return RetrievalPipeline(
        query_processor = QueryProcessor(env.query_config),
        query_rewriter = QueryRewriterManager(env.query_rewrite_config),
        metadata_filter = MetadataFilterManager(env.metadata_filter_config),
        embedding= EmbeddingManager(env.embedding_config),
        vector_store= VectorStoreManager(env.vector_store_config),
        chunk_store= ChunkStoreManager(env.chunk_store_config),
        lexical_search= LexicalSearchManager(env.lexical_search_config),
        hybrid_search= HybridSearchManager(env.hybrid_search_config)
    )

def build_generation_pipeline(storage_dir: Path) -> GenerationPipeline:

    env = build_test_environment(storage_dir)

    retrieval_pipeline = build_retrieval_pipeline(storage_dir)

    return GenerationPipeline(
        query_processor = QueryProcessor(env.query_config),
        retrieval_pipeline = retrieval_pipeline,
        context_builder= ContextBuilder(
            env.context_config
        ),
        prompt_builder=PromptBuilder(),
        llm_manager=LLMManager(
            env.llm_config
        ),
        guardrail_manager=GuardrailManager(
            guardrail_names=(
                "response",
                "grounding"
            )
        ),
        citation_builder=CitationBuilder()

    )
    


        