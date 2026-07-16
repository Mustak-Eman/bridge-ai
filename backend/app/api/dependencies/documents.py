from typing import Annotated

from fastapi import Depends

from app.ai.services.document_analyzer import DocumentAnalyzer
from app.api.dependencies.ai import get_document_analyzer
from app.core.config import Settings, get_settings
from app.documents.parsers.markdown import MarkdownDocumentParser
from app.documents.parsers.pdf import PDFDocumentParser
from app.documents.parsers.text import PlainTextDocumentParser
from app.documents.registry import DocumentParserRegistry
from app.documents.validation import DocumentValidator
from app.services.document_analysis import DocumentAnalysisService


SettingsDependency = Annotated[
    Settings,
    Depends(get_settings),
]


def provide_document_analyzer(
    settings: SettingsDependency,
) -> DocumentAnalyzer:
    return get_document_analyzer(settings)


DocumentAnalyzerDependency = Annotated[
    DocumentAnalyzer,
    Depends(provide_document_analyzer),
]


def get_document_analysis_service(
    settings: SettingsDependency,
    analyzer: DocumentAnalyzerDependency,
) -> DocumentAnalysisService:
    validator = DocumentValidator(
        max_upload_bytes=settings.document_max_upload_bytes
    )

    parser_registry = DocumentParserRegistry(
        [
            PlainTextDocumentParser(),
            MarkdownDocumentParser(),
            PDFDocumentParser(),
        ]
    )

    return DocumentAnalysisService(
        validator=validator,
        parser_registry=parser_registry,
        analyzer=analyzer,
    )


DocumentAnalysisServiceDependency = Annotated[
    DocumentAnalysisService,
    Depends(get_document_analysis_service),
]