from io import BytesIO

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from app.core.exceptions import (
    DocumentParsingError,
    DocumentTextUnavailableError,
    EncryptedDocumentError,
)
from app.documents.models import ParsedDocument, ValidatedDocument


class PDFDocumentParser:
    @property
    def supported_extensions(self) -> frozenset[str]:
        return frozenset({".pdf"})

    def parse(
        self,
        document: ValidatedDocument,
    ) -> ParsedDocument:
        try:
            reader = PdfReader(
                BytesIO(document.content),
                strict=False,
            )
        except (PdfReadError, ValueError, TypeError) as exc:
            raise DocumentParsingError(
                "The uploaded PDF could not be read."
            ) from exc

        if reader.is_encrypted:
            raise EncryptedDocumentError(
                "Encrypted PDF documents are not supported."
            )

        page_text: list[str] = []

        try:
            for page in reader.pages:
                extracted_text = page.extract_text()

                if extracted_text and extracted_text.strip():
                    page_text.append(extracted_text.strip())
        except (PdfReadError, ValueError, TypeError, KeyError) as exc:
            raise DocumentParsingError(
                "Text could not be extracted from the PDF."
            ) from exc

        normalized_text = "\n\n".join(page_text).strip()

        if not normalized_text:
            raise DocumentTextUnavailableError(
                (
                    "The PDF does not contain extractable text. "
                    "Scanned-image PDFs are not currently supported."
                )
            )

        title = self._extract_title(reader)

        return ParsedDocument(
            filename=document.filename,
            extension=document.extension,
            media_type=document.media_type,
            text=normalized_text,
            size_bytes=document.size_bytes,
            character_count=len(normalized_text),
            page_count=len(reader.pages),
            title=title,
        )

    @staticmethod
    def _extract_title(reader: PdfReader) -> str | None:
        metadata = reader.metadata

        if metadata is None:
            return None

        title = metadata.title

        if title is None:
            return None

        normalized_title = str(title).strip()
        return normalized_title or None