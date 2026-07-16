from app.ai.models import DocumentAnalysisResult
from app.ai.services.document_analyzer import DocumentAnalyzer
from app.documents.registry import DocumentParserRegistry
from app.documents.validation import DocumentValidator


class DocumentAnalysisService:
    def __init__(
        self,
        *,
        validator: DocumentValidator,
        parser_registry: DocumentParserRegistry,
        analyzer: DocumentAnalyzer,
    ) -> None:
        self._validator = validator
        self._parser_registry = parser_registry
        self._analyzer = analyzer

    async def analyze_document(
        self,
        *,
        filename: str | None,
        media_type: str | None,
        content: bytes,
    ) -> DocumentAnalysisResult:
        validated_document = self._validator.validate(
            filename=filename,
            media_type=media_type,
            content=content,
        )

        parsed_document = self._parser_registry.parse(
            validated_document
        )

        return await self._analyzer.analyze(
            parsed_document
        )