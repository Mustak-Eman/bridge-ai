import pytest
from pydantic import BaseModel

from app.ai.models import DocumentAnalysis
from app.ai.providers.base import LLMProvider
from app.ai.providers.fake import FakeLLMProvider
from app.core.exceptions import AIStructuredOutputError


class UnsupportedResponseModel(BaseModel):
    value: str


@pytest.mark.anyio
async def test_fake_provider_exposes_provider_metadata() -> None:
    provider = FakeLLMProvider(
        model_name="fake-test-model"
    )

    assert provider.provider_name == "fake"
    assert provider.model_name == "fake-test-model"


@pytest.mark.anyio
async def test_fake_provider_returns_document_analysis() -> None:
    provider = FakeLLMProvider()

    result = await provider.generate_structured(
        system_prompt="Analyze the document.",
        user_prompt=(
            "Applicants must be at least 18 years old. "
            "Applications are due July 31. "
            "Government-issued identification is required. "
            "Late applications may be rejected."
        ),
        response_model=DocumentAnalysis,
    )

    assert isinstance(result, DocumentAnalysis)
    assert result.eligibility_requirements
    assert result.important_deadlines
    assert result.required_documents == [
        "Government-issued identification"
    ]
    assert result.risks
    assert result.key_action_items[0].priority == "high"


@pytest.mark.anyio
async def test_fake_provider_omits_unsupported_facts() -> None:
    provider = FakeLLMProvider()

    result = await provider.generate_structured(
        system_prompt="Analyze the document.",
        user_prompt="This document contains general program guidance.",
        response_model=DocumentAnalysis,
    )

    assert result.eligibility_requirements == []
    assert result.important_deadlines == []
    assert result.required_documents == []
    assert result.risks == []
    assert result.key_action_items == []
    assert result.recommended_next_steps == [
        "Review the document with the responsible program staff."
    ]


@pytest.mark.anyio
async def test_fake_provider_rejects_unsupported_response_model() -> None:
    provider = FakeLLMProvider()

    with pytest.raises(AIStructuredOutputError):
        await provider.generate_structured(
            system_prompt="System prompt",
            user_prompt="User prompt",
            response_model=UnsupportedResponseModel,
        )


def test_fake_provider_satisfies_provider_protocol() -> None:
    provider: LLMProvider = FakeLLMProvider()

    assert provider.provider_name == "fake"