from app.core.exceptions import (
    DocumentEncodingError,
    EmptyDocumentError,
)
from app.documents.models import ParsedDocument, ValidatedDocument


class PlainTextDocumentParser:
    @property
    def supported_extensions(self) -> frozenset[str]:
        return frozenset({".txt"})

    def parse(
        self,
        document: ValidatedDocument,
    ) -> ParsedDocument:
        try:
            text = document.content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise DocumentEncodingError(
                "TXT documents must use UTF-8 encoding."
            ) from exc

        normalized_text = text.strip()

        if not normalized_text:
            raise EmptyDocumentError(
                "The uploaded document does not contain readable text."
            )

        return ParsedDocument(
            filename=document.filename,
            extension=document.extension,
            media_type=document.media_type,
            text=normalized_text,
            size_bytes=document.size_bytes,
            character_count=len(normalized_text),
        )