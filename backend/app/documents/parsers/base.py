from typing import Protocol

from app.documents.models import ParsedDocument, ValidatedDocument


class DocumentParser(Protocol):
    @property
    def supported_extensions(self) -> frozenset[str]:
        """Return the extensions supported by this parser."""

    def parse(
        self,
        document: ValidatedDocument,
    ) -> ParsedDocument:
        """Extract normalized text and metadata from a document."""