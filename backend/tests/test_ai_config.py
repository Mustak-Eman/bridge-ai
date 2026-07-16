import pytest
from pydantic import ValidationError

from app.ai.types import AIProvider
from app.core.config import Settings


def test_settings_default_to_fake_provider() -> None:
    settings = Settings(
        _env_file=None,
    )

    assert settings.ai_provider is AIProvider.FAKE
    assert settings.ai_model == "fake-document-analyzer-v1"
    assert settings.anthropic_api_key is None


def test_settings_accept_anthropic_provider() -> None:
    settings = Settings(
        _env_file=None,
        ai_provider="anthropic",
        ai_model="claude-test-model",
    )

    assert settings.ai_provider is AIProvider.ANTHROPIC
    assert settings.ai_model == "claude-test-model"


def test_settings_reject_unknown_provider() -> None:
    with pytest.raises(ValidationError):
        Settings(
            _env_file=None,
            ai_provider="unknown-provider",
        )