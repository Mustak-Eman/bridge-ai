import pytest

from app.core.exceptions import (
    DocumentTooLargeError,
    EmptyDocumentError,
    UnsupportedDocumentTypeError,
)
from app.documents.validation import DocumentValidator


def test_validator_accepts_txt_document() -> None:
    validator = DocumentValidator(max_upload_bytes=100)

    document = validator.validate(
        filename="policy.txt",
        media_type="text/plain",
        content=b"Community program policy",
    )

    assert document.filename == "policy.txt"
    assert document.extension == ".txt"
    assert document.size_bytes == 24


def test_validator_accepts_markdown_document() -> None:
    validator = DocumentValidator(max_upload_bytes=100)

    document = validator.validate(
        filename="guide.md",
        media_type="text/markdown",
        content=b"# Program Guide",
    )

    assert document.extension == ".md"


def test_validator_removes_directory_components_from_filename() -> None:
    validator = DocumentValidator(max_upload_bytes=100)

    document = validator.validate(
        filename="../../policy.txt",
        media_type="text/plain",
        content=b"Policy",
    )

    assert document.filename == "policy.txt"


def test_validator_rejects_unsupported_extension() -> None:
    validator = DocumentValidator(max_upload_bytes=100)

    with pytest.raises(UnsupportedDocumentTypeError):
        validator.validate(
            filename="policy.docx",
            media_type=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            content=b"content",
        )


def test_validator_rejects_incompatible_media_type() -> None:
    validator = DocumentValidator(max_upload_bytes=100)

    with pytest.raises(UnsupportedDocumentTypeError):
        validator.validate(
            filename="policy.txt",
            media_type="application/pdf",
            content=b"content",
        )


def test_validator_rejects_empty_content() -> None:
    validator = DocumentValidator(max_upload_bytes=100)

    with pytest.raises(EmptyDocumentError):
        validator.validate(
            filename="policy.txt",
            media_type="text/plain",
            content=b"",
        )


def test_validator_rejects_oversized_content() -> None:
    validator = DocumentValidator(max_upload_bytes=4)

    with pytest.raises(DocumentTooLargeError):
        validator.validate(
            filename="policy.txt",
            media_type="text/plain",
            content=b"12345",
        )


def test_validator_rejects_missing_filename() -> None:
    validator = DocumentValidator(max_upload_bytes=100)

    with pytest.raises(UnsupportedDocumentTypeError):
        validator.validate(
            filename=None,
            media_type="text/plain",
            content=b"content",
        )


def test_validator_requires_positive_size_limit() -> None:
    with pytest.raises(ValueError):
        DocumentValidator(max_upload_bytes=0)

def test_validator_accepts_pdf_document() -> None:
    validator = DocumentValidator(max_upload_bytes=100)

    document = validator.validate(
        filename="policy.pdf",
        media_type="application/pdf",
        content=b"%PDF-1.7 sample",
    )

    assert document.extension == ".pdf"
    assert document.media_type == "application/pdf"


def test_validator_rejects_spoofed_pdf() -> None:
    validator = DocumentValidator(max_upload_bytes=100)

    with pytest.raises(UnsupportedDocumentTypeError):
        validator.validate(
            filename="policy.pdf",
            media_type="application/pdf",
            content=b"This is not actually a PDF.",
        )    