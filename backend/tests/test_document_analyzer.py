import pytest

from app.ai.models import DocumentAnalysis
from app.ai.prompts.document_analysis import (
    DOCUMENT_ANALYSIS_PROMPT,
    DOCUMENT_ANALYSIS_PROMPT_NAME,
    DOCUMENT_ANALYSIS_PROMPT_VERSION,
)
from app.ai.prompts.registry import PromptRegistry
from app.ai.providers.fake import FakeLLMProvider
from app.ai.services.document_analyzer import DocumentAnalyzer
from app.core.exceptions import DocumentContentTooLargeError
from app.documents.models import ParsedDocument


def make_document(
    text: str = (
        "Applicants must be at least 18 years old. "
        "Applications are due July 31. "
        "Government-issued identification is required."
    ),
) -> ParsedDocument:
    return ParsedDocument(
        filename="program.txt",
        extension=".txt",
        media_type="text/plain",
        text=text,
        size_bytes=len(text.encode("utf-8")),
        character_count=len(text),
    )


def make_analyzer(
    *,
    max_document_characters: int = 50_000,
) -> DocumentAnalyzer:
    return DocumentAnalyzer(
        provider=FakeLLMProvider(
            model_name="fake-test-model"
        ),
        prompt_registry=PromptRegistry(
            [DOCUMENT_ANALYSIS_PROMPT]
        ),
        max_document_characters=max_document_characters,
    )


@pytest.mark.anyio
async def test_analyzer_returns_structured_analysis() -> None:
    analyzer = make_analyzer()

    result = await analyzer.analyze(make_document())

    assert isinstance(result.analysis, DocumentAnalysis)
    assert result.analysis.eligibility_requirements
    assert result.analysis.important_deadlines
    assert result.analysis.required_documents == [
        "Government-issued identification"
    ]


@pytest.mark.anyio
async def test_analyzer_returns_provider_metadata() -> None:
    analyzer = make_analyzer()

    result = await analyzer.analyze(make_document())

    assert result.metadata.provider == "fake"
    assert result.metadata.model == "fake-test-model"


@pytest.mark.anyio
async def test_analyzer_returns_prompt_metadata() -> None:
    analyzer = make_analyzer()

    result = await analyzer.analyze(make_document())

    assert (
        result.metadata.prompt_name
        == DOCUMENT_ANALYSIS_PROMPT_NAME
    )
    assert (
        result.metadata.prompt_version
        == DOCUMENT_ANALYSIS_PROMPT_VERSION
    )


@pytest.mark.anyio
async def test_analyzer_rejects_excessive_document_text() -> None:
    analyzer = make_analyzer(
        max_document_characters=10
    )
    document = make_document(
        text="This document is longer than ten characters."
    )

    with pytest.raises(DocumentContentTooLargeError):
        await analyzer.analyze(document)


def test_analyzer_requires_positive_character_limit() -> None:
    with pytest.raises(ValueError):
        make_analyzer(
            max_document_characters=0
        )
        
from typing import TypeVar

from pydantic import BaseModel


StructuredOutputT = TypeVar(
    "StructuredOutputT",
    bound=BaseModel,
)


class RecordingProvider:
    def __init__(self) -> None:
        self.system_prompt: str | None = None
        self.user_prompt: str | None = None
        self.response_model: type[BaseModel] | None = None

    @property
    def provider_name(self) -> str:
        return "recording"

    @property
    def model_name(self) -> str:
        return "recording-model"

    async def generate_structured(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_model: type[StructuredOutputT],
    ) -> StructuredOutputT:
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.response_model = response_model

        return response_model(
            executive_summary="Recorded analysis."
        )
        
@pytest.mark.anyio
async def test_analyzer_calls_provider_with_registered_prompt() -> None:
    provider = RecordingProvider()
    analyzer = DocumentAnalyzer(
        provider=provider,
        prompt_registry=PromptRegistry(
            [DOCUMENT_ANALYSIS_PROMPT]
        ),
        max_document_characters=50_000,
    )

    result = await analyzer.analyze(make_document())

    assert provider.system_prompt == (
        DOCUMENT_ANALYSIS_PROMPT.system_prompt
    )
    assert provider.user_prompt is not None
    assert "program.txt" in provider.user_prompt
    assert "Applicants must be at least 18 years old." in (
        provider.user_prompt
    )
    assert provider.response_model is DocumentAnalysis
    assert result.analysis.executive_summary == "Recorded analysis."