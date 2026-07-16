import pytest

from io import BytesIO

from pypdf import PdfWriter
from pypdf.generic import (
    DictionaryObject,
    NameObject,
    RectangleObject,
    StreamObject,
)

from app.core.exceptions import (
    DocumentEncodingError,
    DocumentParsingError,
    DocumentTextUnavailableError,
    EmptyDocumentError,
    EncryptedDocumentError,
    UnsupportedDocumentTypeError,
)
from app.documents.parsers.pdf import PDFDocumentParser

from app.core.exceptions import (
    DocumentEncodingError,
    EmptyDocumentError,
    UnsupportedDocumentTypeError,
)
from app.documents.models import ValidatedDocument
from app.documents.parsers.markdown import MarkdownDocumentParser
from app.documents.parsers.text import PlainTextDocumentParser
from app.documents.registry import DocumentParserRegistry

from pathlib import Path


FIXTURES_DIR = Path(__file__).parent / "fixtures"

def make_document(
    *,
    filename: str,
    extension: str,
    media_type: str,
    content: bytes,
) -> ValidatedDocument:
    return ValidatedDocument(
        filename=filename,
        extension=extension,
        media_type=media_type,
        content=content,
        size_bytes=len(content),
    )


def test_plain_text_parser_extracts_text() -> None:
    parser = PlainTextDocumentParser()
    document = make_document(
        filename="policy.txt",
        extension=".txt",
        media_type="text/plain",
        content=b"  Program eligibility requirements.  ",
    )

    parsed = parser.parse(document)

    assert parsed.text == "Program eligibility requirements."
    assert parsed.character_count == len(parsed.text)
    assert parsed.title is None


def test_plain_text_parser_rejects_invalid_utf8() -> None:
    parser = PlainTextDocumentParser()
    document = make_document(
        filename="policy.txt",
        extension=".txt",
        media_type="text/plain",
        content=b"\xff\xfe\xfa",
    )

    with pytest.raises(DocumentEncodingError):
        parser.parse(document)


def test_plain_text_parser_rejects_whitespace_only_content() -> None:
    parser = PlainTextDocumentParser()
    document = make_document(
        filename="policy.txt",
        extension=".txt",
        media_type="text/plain",
        content=b"   \n\t ",
    )

    with pytest.raises(EmptyDocumentError):
        parser.parse(document)


def test_markdown_parser_extracts_first_level_heading() -> None:
    parser = MarkdownDocumentParser()
    document = make_document(
        filename="guide.md",
        extension=".md",
        media_type="text/markdown",
        content=(
            b"# Workforce Program\n\n"
            b"Applicants must be at least 18."
        ),
    )

    parsed = parser.parse(document)

    assert parsed.title == "Workforce Program"
    assert "# Workforce Program" in parsed.text


def test_markdown_parser_returns_no_title_without_h1() -> None:
    parser = MarkdownDocumentParser()
    document = make_document(
        filename="guide.md",
        extension=".md",
        media_type="text/markdown",
        content=b"## Eligibility\n\nApplicants must be 18.",
    )

    parsed = parser.parse(document)

    assert parsed.title is None


def test_registry_selects_parser_by_extension() -> None:
    registry = DocumentParserRegistry(
        [
            PlainTextDocumentParser(),
            MarkdownDocumentParser(),
        ]
    )
    document = make_document(
        filename="guide.md",
        extension=".md",
        media_type="text/markdown",
        content=b"# Guide",
    )

    parsed = registry.parse(document)

    assert parsed.title == "Guide"


def test_registry_rejects_missing_parser() -> None:
    registry = DocumentParserRegistry(
        [PlainTextDocumentParser()]
    )
    document = make_document(
        filename="guide.md",
        extension=".md",
        media_type="text/markdown",
        content=b"# Guide",
    )

    with pytest.raises(UnsupportedDocumentTypeError):
        registry.parse(document)


def test_registry_rejects_duplicate_extension_registration() -> None:
    with pytest.raises(ValueError):
        DocumentParserRegistry(
            [
                PlainTextDocumentParser(),
                PlainTextDocumentParser(),
            ]
        )

def make_blank_pdf(*, encrypted: bool = False) -> bytes:
    output = BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)

    if encrypted:
        writer.encrypt("secret")

    writer.write(output)
    return output.getvalue()

def test_pdf_parser_rejects_pdf_without_extractable_text() -> None:
    parser = PDFDocumentParser()
    content = make_blank_pdf()
    document = make_document(
        filename="blank.pdf",
        extension=".pdf",
        media_type="application/pdf",
        content=content,
    )

    with pytest.raises(DocumentTextUnavailableError):
        parser.parse(document)


def test_pdf_parser_rejects_encrypted_pdf() -> None:
    parser = PDFDocumentParser()
    content = make_blank_pdf(encrypted=True)
    document = make_document(
        filename="encrypted.pdf",
        extension=".pdf",
        media_type="application/pdf",
        content=content,
    )

    with pytest.raises(EncryptedDocumentError):
        parser.parse(document)


def test_pdf_parser_rejects_malformed_pdf() -> None:
    parser = PDFDocumentParser()
    document = make_document(
        filename="broken.pdf",
        extension=".pdf",
        media_type="application/pdf",
        content=b"%PDF-1.7\nnot a valid PDF",
    )

    with pytest.raises(DocumentParsingError):
        parser.parse(document)
        
def test_registry_registers_pdf_parser() -> None:
    registry = DocumentParserRegistry(
        [
            PlainTextDocumentParser(),
            MarkdownDocumentParser(),
            PDFDocumentParser(),
        ]
    )
    content = make_blank_pdf()
    document = make_document(
        filename="blank.pdf",
        extension=".pdf",
        media_type="application/pdf",
        content=content,
    )

    with pytest.raises(DocumentTextUnavailableError):
        registry.parse(document)    
        
def test_pdf_parser_extracts_text_and_metadata() -> None:
    parser = PDFDocumentParser()
    content = (
        FIXTURES_DIR / "sample_text.pdf"
    ).read_bytes()
    document = make_document(
        filename="program.pdf",
        extension=".pdf",
        media_type="application/pdf",
        content=content,
    )

    parsed = parser.parse(document)

    assert "Community workforce program guidelines." in parsed.text
    assert parsed.page_count == 1
    assert parsed.title == "Workforce Program Guidelines"
    assert parsed.character_count == len(parsed.text)