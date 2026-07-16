from pathlib import Path

import pytest

from app.ai.prompts.document_analysis import (
    DOCUMENT_ANALYSIS_PROMPT,
)
from app.ai.prompts.registry import PromptRegistry
from app.ai.providers.fake import FakeLLMProvider
from app.ai.services.document_analyzer import DocumentAnalyzer
from app.core.exceptions import (
    DocumentContentTooLargeError,
    DocumentEncodingError,
    DocumentTextUnavailableError,
    EmptyDocumentError,
    UnsupportedDocumentTypeError,
)
from app.documents.parsers.markdown import MarkdownDocumentParser
from app.documents.parsers.pdf import PDFDocumentParser
from app.documents.parsers.text import PlainTextDocumentParser
from app.documents.registry import DocumentParserRegistry
from app.documents.validation import DocumentValidator
from app.services.document_analysis import DocumentAnalysisService

from app.ai.models import (
    AIAnalysisMetadata,
    DocumentAnalysis,
    DocumentAnalysisResult,
)
from app.documents.models import ParsedDocument


class RecordingAnalyzer:
    def __init__(self) -> None:
        self.calls = 0
        self.document: ParsedDocument | None = None

    async def analyze(
        self,
        document: ParsedDocument,
    ) -> DocumentAnalysisResult:
        self.calls += 1
        self.document = document

        return DocumentAnalysisResult(
            analysis=DocumentAnalysis(
                executive_summary="Recorded analysis."
            ),
            metadata=AIAnalysisMetadata(
                prompt_name="recording-prompt",
                prompt_version="1.0",
                provider="recording",
                model="recording-model",
            ),
        )
        
FIXTURES_DIR = Path(__file__).parent / "fixtures"


def make_service(
    *,
    max_upload_bytes: int = 5_000_000,
    max_document_characters: int = 50_000,
) -> DocumentAnalysisService:
    validator = DocumentValidator(
        max_upload_bytes=max_upload_bytes
    )

    parser_registry = DocumentParserRegistry(
        [
            PlainTextDocumentParser(),
            MarkdownDocumentParser(),
            PDFDocumentParser(),
        ]
    )

    analyzer = DocumentAnalyzer(
        provider=FakeLLMProvider(
            model_name="fake-service-test-model"
        ),
        prompt_registry=PromptRegistry(
            [DOCUMENT_ANALYSIS_PROMPT]
        ),
        max_document_characters=max_document_characters,
    )

    return DocumentAnalysisService(
        validator=validator,
        parser_registry=parser_registry,
        analyzer=analyzer,
    )


@pytest.mark.anyio
async def test_service_analyzes_txt_document() -> None:
    service = make_service()
    content = (
        b"Applicants must be at least 18 years old. "
        b"Applications are due July 31. "
        b"Government-issued identification is required."
    )

    result = await service.analyze_document(
        filename="program.txt",
        media_type="text/plain",
        content=content,
    )

    assert result.analysis.eligibility_requirements
    assert result.analysis.important_deadlines
    assert result.analysis.required_documents == [
        "Government-issued identification"
    ]
    assert result.metadata.provider == "fake"
    assert result.metadata.model == "fake-service-test-model"


@pytest.mark.anyio
async def test_service_analyzes_markdown_document() -> None:
    service = make_service()
    content = (
        b"# Workforce Program\n\n"
        b"Applicants must be at least 18 years old."
    )

    result = await service.analyze_document(
        filename="program.md",
        media_type="text/markdown",
        content=content,
    )

    assert result.analysis.eligibility_requirements
    assert result.metadata.prompt_name == (
        "document_operational_analysis"
    )


@pytest.mark.anyio
async def test_service_analyzes_pdf_document() -> None:
    service = make_service()
    content = (
        FIXTURES_DIR / "sample_text.pdf"
    ).read_bytes()

    result = await service.analyze_document(
        filename="program.pdf",
        media_type="application/pdf",
        content=content,
    )

    assert result.analysis.executive_summary
    assert result.metadata.provider == "fake"


@pytest.mark.anyio
async def test_service_rejects_unsupported_document() -> None:
    service = make_service()

    with pytest.raises(UnsupportedDocumentTypeError):
        await service.analyze_document(
            filename="program.docx",
            media_type=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            content=b"Document content",
        )


@pytest.mark.anyio
async def test_service_rejects_empty_document() -> None:
    service = make_service()

    with pytest.raises(EmptyDocumentError):
        await service.analyze_document(
            filename="program.txt",
            media_type="text/plain",
            content=b"",
        )


@pytest.mark.anyio
async def test_service_rejects_invalid_text_encoding() -> None:
    service = make_service()

    with pytest.raises(DocumentEncodingError):
        await service.analyze_document(
            filename="program.txt",
            media_type="text/plain",
            content=b"\xff\xfe\xfa",
        )


@pytest.mark.anyio
async def test_service_rejects_pdf_without_text() -> None:
    service = make_service()
    content = (
        FIXTURES_DIR / "blank.pdf"
    ).read_bytes()

    with pytest.raises(DocumentTextUnavailableError):
        await service.analyze_document(
            filename="blank.pdf",
            media_type="application/pdf",
            content=content,
        )


@pytest.mark.anyio
async def test_service_rejects_excessive_extracted_text() -> None:
    service = make_service(
        max_document_characters=10
    )

    with pytest.raises(DocumentContentTooLargeError):
        await service.analyze_document(
            filename="program.txt",
            media_type="text/plain",
            content=b"This text is longer than ten characters.",
        )
        
@pytest.mark.anyio
async def test_service_passes_parsed_document_to_analyzer() -> None:
    analyzer = RecordingAnalyzer()
    service = DocumentAnalysisService(
        validator=DocumentValidator(
            max_upload_bytes=1_000
        ),
        parser_registry=DocumentParserRegistry(
            [PlainTextDocumentParser()]
        ),
        analyzer=analyzer,
    )

    result = await service.analyze_document(
        filename="policy.txt",
        media_type="text/plain",
        content=b"  Program policy content.  ",
    )

    assert analyzer.calls == 1
    assert analyzer.document is not None
    assert analyzer.document.text == "Program policy content."
    assert result.metadata.provider == "recording"


@pytest.mark.anyio
async def test_service_does_not_call_analyzer_when_validation_fails() -> None:
    analyzer = RecordingAnalyzer()
    service = DocumentAnalysisService(
        validator=DocumentValidator(
            max_upload_bytes=1_000
        ),
        parser_registry=DocumentParserRegistry(
            [PlainTextDocumentParser()]
        ),
        analyzer=analyzer,
    )

    with pytest.raises(UnsupportedDocumentTypeError):
        await service.analyze_document(
            filename="policy.exe",
            media_type="application/octet-stream",
            content=b"content",
        )

    assert analyzer.calls == 0