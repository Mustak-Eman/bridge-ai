from app.core.exceptions import UnsupportedDocumentTypeError
from app.documents.models import ParsedDocument, ValidatedDocument
from app.documents.parsers.base import DocumentParser


class DocumentParserRegistry:
    def __init__(
        self,
        parsers: list[DocumentParser],
    ) -> None:
        self._parsers: dict[str, DocumentParser] = {}

        for parser in parsers:
            for extension in parser.supported_extensions:
                normalized_extension = extension.lower()

                if normalized_extension in self._parsers:
                    raise ValueError(
                        (
                            "Multiple document parsers are registered for "
                            f"extension '{normalized_extension}'."
                        )
                    )

                self._parsers[normalized_extension] = parser

    def parse(
        self,
        document: ValidatedDocument,
    ) -> ParsedDocument:
        parser = self._parsers.get(document.extension.lower())

        if parser is None:
            raise UnsupportedDocumentTypeError(
                (
                    "No parser is registered for document extension "
                    f"'{document.extension}'."
                )
            )

        return parser.parse(document)