import pytest

from app.ai.prompts.base import PromptDefinition
from app.ai.prompts.document_analysis import (
    DOCUMENT_ANALYSIS_PROMPT,
    DOCUMENT_ANALYSIS_PROMPT_NAME,
    DOCUMENT_ANALYSIS_PROMPT_VERSION,
    build_document_analysis_user_prompt,
)
from app.ai.prompts.registry import (
    PromptNotFoundError,
    PromptRegistry,
)
from app.documents.models import ParsedDocument


def make_parsed_document() -> ParsedDocument:
    text = (
        "# Workforce Program\n\n"
        "Applicants must be at least 18 years old.\n"
        "Applications are due July 31."
    )

    return ParsedDocument(
        filename="program.md",
        extension=".md",
        media_type="text/markdown",
        text=text,
        size_bytes=len(text.encode("utf-8")),
        character_count=len(text),
        title="Workforce Program",
    )


def test_document_analysis_prompt_has_stable_identity() -> None:
    assert (
        DOCUMENT_ANALYSIS_PROMPT.name
        == DOCUMENT_ANALYSIS_PROMPT_NAME
    )
    assert (
        DOCUMENT_ANALYSIS_PROMPT.version
        == DOCUMENT_ANALYSIS_PROMPT_VERSION
    )
    assert DOCUMENT_ANALYSIS_PROMPT.version == "1.0"


def test_document_analysis_system_prompt_requires_grounded_output() -> None:
    system_prompt = DOCUMENT_ANALYSIS_PROMPT.system_prompt.lower()

    assert "do not invent" in system_prompt
    assert "provided document" in system_prompt
    assert "structured schema" in system_prompt


def test_user_prompt_contains_document_metadata_and_content() -> None:
    document = make_parsed_document()

    user_prompt = build_document_analysis_user_prompt(
        document=document
    )

    assert "program.md" in user_prompt
    assert "text/markdown" in user_prompt
    assert "Workforce Program" in user_prompt
    assert "Applicants must be at least 18 years old." in user_prompt
    assert "----- BEGIN DOCUMENT -----" in user_prompt
    assert "----- END DOCUMENT -----" in user_prompt


def test_user_prompt_handles_missing_optional_metadata() -> None:
    document = ParsedDocument(
        filename="policy.txt",
        extension=".txt",
        media_type="text/plain",
        text="Program policy.",
        size_bytes=15,
        character_count=15,
    )

    user_prompt = build_document_analysis_user_prompt(
        document=document
    )

    assert "Title: Not provided" in user_prompt
    assert "Page count: Not applicable" in user_prompt


def test_registry_returns_registered_prompt() -> None:
    registry = PromptRegistry([DOCUMENT_ANALYSIS_PROMPT])

    prompt = registry.get(DOCUMENT_ANALYSIS_PROMPT_NAME)

    assert prompt is DOCUMENT_ANALYSIS_PROMPT


def test_registry_rejects_unknown_prompt() -> None:
    registry = PromptRegistry([DOCUMENT_ANALYSIS_PROMPT])

    with pytest.raises(PromptNotFoundError):
        registry.get("missing_prompt")


def test_registry_rejects_duplicate_prompt_names() -> None:
    duplicate = PromptDefinition(
        name=DOCUMENT_ANALYSIS_PROMPT_NAME,
        version="2.0",
        system_prompt="Different instructions.",
        build_user_prompt=lambda: "Different prompt.",
    )

    with pytest.raises(ValueError):
        PromptRegistry(
            [
                DOCUMENT_ANALYSIS_PROMPT,
                duplicate,
            ]
        )