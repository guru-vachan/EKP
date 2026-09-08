from __future__ import annotations

class EKIPException(Exception):
    """
        Base exception for the Enterprise Knowledge Intelligent Platform.
    """

# ============================
# Configuration
# ============================

class ConfigurationError(EKIPException):
    """ 
        Raised when application configuration is invalid.
    """

# ============================
# Ingestion
# ============================

class IngestionError(EKIPException):
    """ """


class UnsupportedFileTypeError(IngestionError):
    """ """


class DocumentLoadingError(IngestionError):
    """ """

class MetadataGenerationError(IngestionError):
    """ """

# ============================
# Chunking
# ============================

class ChunkingError(EKIPException):
    """ """

class UnsupportedChunkingStrategy(ChunkingError):
    """ """

# ============================
# EMbeddings
# ============================

class EmbeddingError(EKIPException):
    """ """

class UnsupportedEmbeddingProvider(EmbeddingError):
    """
    """

class EmbeddingGenerationError(EmbeddingError):
    """
    """

# ============================
# Vector Store
# ============================

class VectorStoreError(EKIPException):
    """ """

class UnsupportedVectorStoreProvider(VectorStoreError):
    """ """

class VectorStoreInitializationError(VectorStoreError):
    """ """

class VectorSearchError(VectorStoreError):
    """ """

# ============================
# Query
# ============================

class QueryValidationError(EKIPException):
    """ """