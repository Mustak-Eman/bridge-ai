from functools import lru_cache

from app.ai.prompts.document_analysis import (
    DOCUMENT_ANALYSIS_PROMPT,
)
from app.ai.prompts.registry import PromptRegistry
from app.ai.providers.base import LLMProvider
from app.ai.providers.fake import FakeLLMProvider
from app.ai.services.document_analyzer import DocumentAnalyzer
from app.ai.types import AIProvider
from app.core.config import Settings, get_settings
from app.core.exceptions import AIProviderConfigurationError


@lru_cache
def get_prompt_registry() -> PromptRegistry:
    return PromptRegistry(
        [
            DOCUMENT_ANALYSIS_PROMPT,
        ]
    )


def get_llm_provider(
    settings: Settings,
) -> LLMProvider:
    if settings.ai_provider is AIProvider.FAKE:
        return FakeLLMProvider(
            model_name=settings.ai_model
        )

    if settings.ai_provider is AIProvider.ANTHROPIC:
        raise AIProviderConfigurationError(
            (
                "The Anthropic provider is not enabled in this "
                "deployment. Set AI_PROVIDER=fake to run locally."
            )
        )

    raise AIProviderConfigurationError(
        f"Unsupported AI provider: {settings.ai_provider}."
    )


def get_document_analyzer(
    settings: Settings,
) -> DocumentAnalyzer:
    return DocumentAnalyzer(
        provider=get_llm_provider(settings),
        prompt_registry=get_prompt_registry(),
        max_document_characters=(
            settings.ai_max_document_characters
        ),
    )