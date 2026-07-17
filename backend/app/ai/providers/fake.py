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

        # Existing eligibility behavior retained for current tests.
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

        # Existing deadline behavior retained for current tests.
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

        # General identification-document extraction.
        if (
            "government-issued identification" in prompt_text
            or "government issued identification" in prompt_text
        ):
            required_documents.append(
                "Government-issued identification"
            )

        if "proof of identification" in prompt_text:
            required_documents.append("Proof of identification")

        if "proof of income" in prompt_text:
            required_documents.append("Proof of income")

        if "proof of residence" in prompt_text:
            required_documents.append("Proof of residence")

        # Housing-policy workflow extraction.
        if "incomplete applications" in prompt_text:
            key_action_items.append(
                {
                    "action": (
                        "Review incomplete applications and identify "
                        "missing information."
                    ),
                    "priority": "medium",
                    "owner": "Program staff",
                    "deadline": None,
                }
            )

        if "five business days" in prompt_text:
            important_deadlines.append(
                {
                    "description": (
                        "Review incomplete applications within the "
                        "required processing window."
                    ),
                    "date": "Within five business days",
                    "source_text": (
                        "Incomplete applications should be reviewed "
                        "within five business days."
                    ),
                }
            )

            key_action_items.append(
                {
                    "action": (
                        "Complete the review of incomplete applications "
                        "within five business days."
                    ),
                    "priority": "high",
                    "owner": "Program staff",
                    "deadline": "Within five business days",
                }
            )

        if (
            "notify applicants of missing documents" in prompt_text
            or "notify applicants" in prompt_text
            and "missing documents" in prompt_text
        ):
            key_action_items.append(
                {
                    "action": (
                        "Notify applicants about all missing required "
                        "documents."
                    ),
                    "priority": "high",
                    "owner": "Program staff",
                    "deadline": None,
                }
            )

        if "eviction risk" in prompt_text:
            key_action_items.append(
                {
                    "action": (
                        "Escalate urgent cases involving eviction risk "
                        "to a program supervisor."
                    ),
                    "priority": "high",
                    "owner": "Program staff",
                    "deadline": "Immediately",
                }
            )

            risks.append(
                {
                    "description": (
                        "Applicants facing eviction may experience housing "
                        "loss if urgent cases are not escalated promptly."
                    ),
                    "severity": "high",
                    "mitigation": (
                        "Flag eviction-risk cases immediately and route "
                        "them to a program supervisor."
                    ),
                }
            )

        if "program supervisor" in prompt_text:
            recommended_next_steps.append(
                (
                    "Confirm that staff understand the escalation process "
                    "for urgent cases."
                )
            )

        # Existing risk behavior retained for current tests.
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
                (
                    "Collect and verify all required documents before "
                    "completing the application review."
                )
            )

        if important_deadlines:
            recommended_next_steps.append(
                (
                    "Create reminders and assign staff ownership for all "
                    "identified deadlines."
                )
            )

        if key_action_items:
            recommended_next_steps.append(
                (
                    "Document completion of each action item in the "
                    "applicant case record."
                )
            )

        if not recommended_next_steps:
            recommended_next_steps.append(
                "Review the document with the responsible program staff."
            )

        executive_summary = (
            "This document contains operational guidance for a community "
            "program. Review the extracted requirements, deadlines, and "
            "next steps before taking action."
        )

        if (
            "housing support program" in prompt_text
            or "eviction risk" in prompt_text
            or "proof of residence" in prompt_text
        ):
            executive_summary = (
                "This housing support policy defines required applicant "
                "documents, expectations for reviewing incomplete "
                "applications, applicant notification responsibilities, "
                "and escalation procedures for urgent eviction-risk cases."
            )

        return {
            "executive_summary": executive_summary,
            "key_action_items": FakeLLMProvider._deduplicate_dict_items(
                key_action_items
            ),
            "eligibility_requirements": (
                FakeLLMProvider._deduplicate_dict_items(
                    eligibility_requirements
                )
            ),
            "important_deadlines": (
                FakeLLMProvider._deduplicate_dict_items(
                    important_deadlines
                )
            ),
            "required_documents": FakeLLMProvider._deduplicate_strings(
                required_documents
            ),
            "risks": FakeLLMProvider._deduplicate_dict_items(risks),
            "recommended_next_steps": (
                FakeLLMProvider._deduplicate_strings(
                    recommended_next_steps
                )
            ),
        }

    @staticmethod
    def _deduplicate_strings(items: list[str]) -> list[str]:
        return list(dict.fromkeys(items))

    @staticmethod
    def _deduplicate_dict_items(
        items: list[dict[str, str | None]],
    ) -> list[dict[str, str | None]]:
        unique_items: list[dict[str, str | None]] = []
        seen_items: set[tuple[tuple[str, str | None], ...]] = set()

        for item in items:
            item_key = tuple(sorted(item.items()))

            if item_key in seen_items:
                continue

            seen_items.add(item_key)
            unique_items.append(item)

        return unique_items