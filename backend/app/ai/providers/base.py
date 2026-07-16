from typing import Protocol, TypeVar

from pydantic import BaseModel


StructuredOutputT = TypeVar(
    "StructuredOutputT",
    bound=BaseModel,
)


class LLMProvider(Protocol):
    @property
    def provider_name(self) -> str:
        """Return the provider identifier."""

    @property
    def model_name(self) -> str:
        """Return the configured model identifier."""

    async def generate_structured(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_model: type[StructuredOutputT],
    ) -> StructuredOutputT:
        """Generate and validate a structured response."""