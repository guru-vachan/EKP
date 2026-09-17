import logging

from app.citations.citation_builder import CitationBuilder
from app.guardrail.guardrail_manager import GuardrailManager
from app.llm.llm_manager import LLMManager
from app.llm.prompt_builder import PromptBuilder
from app.retrieval.context_builder.context_builder import ContextBuilder
from app.retrieval.query_processing.query_processor import QueryProcessor
from app.retrieval.retrieval_pipeline import RetrievalPipeline
from app.schemas.final_response import FinalResponse

logger = logging.getLogger(__name__)

class GenerationPipeline:

    def __init__(
        self,
        query_processor: QueryProcessor,
        retrieval_pipeline: RetrievalPipeline,
        context_builder: ContextBuilder,
        prompt_builder: PromptBuilder,
        llm_manager: LLMManager,
        guardrail_manager: GuardrailManager,
        citation_builder: CitationBuilder,

    ) -> None:
        
        self._query_processor=query_processor
        self._retrieval_pipeline= retrieval_pipeline
        self._context_builder= context_builder
        self._prompt_builder= prompt_builder
        self._llm_manager= llm_manager
        self._guardrail_manager= guardrail_manager
        self._citation_builder= citation_builder

    
    def generate(self, raw_query:str) -> FinalResponse:

        query = self._query_processor.process(raw_query)

        search_results = self._retrieval_pipeline.retrieve(query.query)

        context = self._context_builder.build(search_results)

        prompt = self._prompt_builder.build(
            query=query,
            context=context
        )

        llm_response = self._llm_manager.generate(prompt)

        guardrail_result = self._guardrail_manager.validate(
            response=llm_response,
            context=context,
        )

        if not guardrail_result.passed:
            logging.warning("Generation Blocked by guardrail")
            return FinalResponse(
                query_id=query.query_id,
                answer=llm_response.content, # for testing just passed content in both cases.
                citation=[],
                model_name=llm_response.model_name,
                provider=llm_response.provider,
                guardrail_result=guardrail_result,
                usage=llm_response.usage
            )
        
        citations = self._citation_builder.build(
            response=llm_response,
            context=context
        )

        return FinalResponse (
            query_id=query.query_id,
            answer=llm_response.content,
            citation=citations,
            model_name=llm_response.model_name,
            provider=llm_response.provider,
            usage=llm_response.usage,
            guardrail_result=guardrail_result
            )
