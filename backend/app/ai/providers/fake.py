from typing import Any, TypeVar

from pydantic import BaseModel, ValidationError

from app.ai.models import DocumentAnalysis
from app.core.exceptions import AIStructuredOutputError


StructuredOutputT = TypeVar(
    "StructuredOutputT",
    bound=BaseModel,
)


class FakeLLMProvider:
    def __init__(
        self,
        *,
        model_name: str = "fake-document-analyzer-v1",
    ) -> None:
        self._model_name = model_name

    @property
    def provider_name(self) -> str:
        return "fake"

    @property
    def model_name(self) -> str:
        return self._model_name

    async def generate_structured(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_model: type[StructuredOutputT],
    ) -> StructuredOutputT:
        del system_prompt

        response_data = self._build_response_data(
            user_prompt=user_prompt,
            response_model=response_model,
        )

        try:
            return response_model.model_validate(response_data)
        except ValidationError as exc:
            raise AIStructuredOutputError(
                "The fake provider produced invalid structured output."
            ) from exc

    @staticmethod
    def _build_response_data(
        *,
        user_prompt: str,
        response_model: type[BaseModel],
    ) -> dict[str, Any]:
        if response_model is not DocumentAnalysis:
            raise AIStructuredOutputError(
                (
                    "The fake provider does not support the requested "
                    f"response model '{response_model.__name__}'."
                )
            )

        prompt_text = user_prompt.lower()

        eligibility_requirements: list[dict[str, str | None]] = []
        important_deadlines: list[dict[str, str | None]] = []
        required_documents: list[str] = []
        key_action_items: list[dict[str, str | None]] = []
        risks: list[dict[str, str | None]] = []
        recommended_next_steps: list[str] = []

        if "18 years" in prompt_text or "at least 18" in prompt_text:
            eligibility_requirements.append(
                {
                    "requirement": "Applicant must be at least 18 years old.",
                    "evidence": (
                        "The document states that applicants must be "
                        "at least 18 years old."
                    ),
                }
            )

        if "july 31" in prompt_text:
            important_deadlines.append(
                {
                    "description": "Application deadline",
                    "date": "July 31",
                    "source_text": "Applications are due July 31.",
                }
            )
            key_action_items.append(
                {
                    "action": "Submit the application before July 31.",
                    "priority": "high",
                    "owner": None,
                    "deadline": "July 31",
                }
            )

        if (
            "government-issued identification" in prompt_text
            or "government issued identification" in prompt_text
        ):
            required_documents.append(
                "Government-issued identification"
            )

        if "late applications" in prompt_text:
            risks.append(
                {
                    "description": "Late applications may be rejected.",
                    "severity": "high",
                    "mitigation": "Submit before the stated deadline.",
                }
            )

        if eligibility_requirements:
            recommended_next_steps.append(
                "Confirm that the applicant meets the eligibility rules."
            )

        if required_documents:
            recommended_next_steps.append(
                "Collect the required documentation."
            )

        if important_deadlines:
            recommended_next_steps.append(
                "Create a reminder for the application deadline."
            )

        if not recommended_next_steps:
            recommended_next_steps.append(
                "Review the document with the responsible program staff."
            )

        return {
            "executive_summary": (
                "This document contains operational guidance for a "
                "community program. Review the extracted requirements, "
                "deadlines, and next steps before taking action."
            ),
            "key_action_items": key_action_items,
            "eligibility_requirements": eligibility_requirements,
            "important_deadlines": important_deadlines,
            "required_documents": required_documents,
            "risks": risks,
            "recommended_next_steps": recommended_next_steps,
        }