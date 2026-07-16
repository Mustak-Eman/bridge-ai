from pathlib import Path

from app.core.exceptions import (
    DocumentTooLargeError,
    EmptyDocumentError,
    UnsupportedDocumentTypeError,
)
from app.documents.models import ValidatedDocument


SUPPORTED_DOCUMENT_TYPES: dict[str, frozenset[str]] = {
    ".txt": frozenset(
        {
            "text/plain",
            "application/octet-stream",
        }
    ),
    ".md": frozenset(
        {
            "text/markdown",
            "text/plain",
            "application/octet-stream",
        }
    ),
    ".markdown": frozenset(
        {
            "text/markdown",
            "text/plain",
            "application/octet-stream",
        }
    ),
    ".pdf": frozenset(
        {
            "application/pdf",
            "application/octet-stream",
        }
    ),
}


class DocumentValidator:
    def __init__(self, *, max_upload_bytes: int) -> None:
        if max_upload_bytes <= 0:
            raise ValueError("max_upload_bytes must be greater than zero")

        self._max_upload_bytes = max_upload_bytes

    def validate(
        self,
        *,
        filename: str | None,
        media_type: str | None,
        content: bytes,
    ) -> ValidatedDocument:
        normalized_filename = self._validate_filename(filename)
        extension = Path(normalized_filename).suffix.lower()

        allowed_media_types = SUPPORTED_DOCUMENT_TYPES.get(extension)

        if allowed_media_types is None:
            raise UnsupportedDocumentTypeError(
                "Only PDF, TXT, and Markdown documents are supported."
            )

        normalized_media_type = (
            media_type.lower().strip()
            if media_type
            else "application/octet-stream"
        )

        if normalized_media_type not in allowed_media_types:
            raise UnsupportedDocumentTypeError(
                (
                    f"Media type '{normalized_media_type}' is not valid "
                    f"for '{extension}' documents."
                )
            )

        size_bytes = len(content)

        if size_bytes == 0:
            raise EmptyDocumentError("The uploaded document is empty.")

        if size_bytes > self._max_upload_bytes:
            raise DocumentTooLargeError(
                (
                    "The uploaded document exceeds the maximum size of "
                    f"{self._max_upload_bytes} bytes."
                )
            )
        
        if extension == ".pdf" and not content.startswith(b"%PDF-"):
            raise UnsupportedDocumentTypeError(
        "The uploaded file does not contain a valid PDF signature."
        )

        return ValidatedDocument(
            filename=normalized_filename,
            extension=extension,
            media_type=normalized_media_type,
            content=content,
            size_bytes=size_bytes,
        )

    @staticmethod
    def _validate_filename(filename: str | None) -> str:
        if filename is None or not filename.strip():
            raise UnsupportedDocumentTypeError(
                "The uploaded document must have a filename."
            )

        normalized_filename = Path(filename.strip()).name

        if not normalized_filename:
            raise UnsupportedDocumentTypeError(
                "The uploaded document must have a valid filename."
            )

        return normalized_filename