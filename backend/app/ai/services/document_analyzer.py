from app.ai.models import (
    AIAnalysisMetadata,
    DocumentAnalysis,
    DocumentAnalysisResult,
)
from app.ai.prompts.document_analysis import (
    DOCUMENT_ANALYSIS_PROMPT_NAME,
)
from app.ai.prompts.registry import PromptRegistry
from app.ai.providers.base import LLMProvider
from app.core.exceptions import DocumentContentTooLargeError
from app.documents.models import ParsedDocument


class DocumentAnalyzer:
    def __init__(
        self,
        *,
        provider: LLMProvider,
        prompt_registry: PromptRegistry,
        max_document_characters: int,
    ) -> None:
        if max_document_characters <= 0:
            raise ValueError(
                "max_document_characters must be greater than zero"
            )

        self._provider = provider
        self._prompt_registry = prompt_registry
        self._max_document_characters = max_document_characters

    async def analyze(
        self,
        document: ParsedDocument,
    ) -> DocumentAnalysisResult:
        self._validate_document_length(document)

        prompt = self._prompt_registry.get(
            DOCUMENT_ANALYSIS_PROMPT_NAME
        )

        user_prompt = prompt.build_user_prompt(
            document=document
        )

        analysis = await self._provider.generate_structured(
            system_prompt=prompt.system_prompt,
            user_prompt=user_prompt,
            response_model=DocumentAnalysis,
        )

        return DocumentAnalysisResult(
            analysis=analysis,
            metadata=AIAnalysisMetadata(
                prompt_name=prompt.name,
                prompt_version=prompt.version,
                provider=self._provider.provider_name,
                model=self._provider.model_name,
            ),
        )

    def _validate_document_length(
        self,
        document: ParsedDocument,
    ) -> None:
        if document.character_count > self._max_document_characters:
            raise DocumentContentTooLargeError(
                (
                    "The extracted document text exceeds the maximum "
                    f"AI processing limit of "
                    f"{self._max_document_characters} characters."
                )
            )