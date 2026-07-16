import pytest

from app.ai.providers.fake import FakeLLMProvider
from app.ai.types import AIProvider
from app.api.dependencies.ai import (
    get_document_analyzer,
    get_llm_provider,
)
from app.core.config import Settings
from app.core.exceptions import AIProviderConfigurationError


def make_settings(
    *,
    ai_provider: str = "fake",
    ai_model: str = "fake-test-model",
) -> Settings:
    return Settings(
        _env_file=None,
        ai_provider=ai_provider,
        ai_model=ai_model,
    )


def test_get_llm_provider_returns_fake_provider() -> None:
    settings = make_settings()

    provider = get_llm_provider(settings)

    assert isinstance(provider, FakeLLMProvider)
    assert provider.provider_name == "fake"
    assert provider.model_name == "fake-test-model"


def test_get_document_analyzer_returns_analyzer() -> None:
    settings = make_settings()

    analyzer = get_document_analyzer(settings)

    assert analyzer is not None


def test_anthropic_provider_fails_clearly_when_not_enabled() -> None:
    settings = make_settings(
        ai_provider=AIProvider.ANTHROPIC,
        ai_model="claude-test-model",
    )

    with pytest.raises(AIProviderConfigurationError):
        get_llm_provider(settings)