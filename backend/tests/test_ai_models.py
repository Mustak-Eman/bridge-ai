import pytest
from pydantic import ValidationError

from app.ai.models import DocumentAnalysis


def valid_analysis_data() -> dict:
    return {
        "executive_summary": "The program provides workforce training.",
        "key_action_items": [
            {
                "action": "Submit the application.",
                "priority": "high",
                "owner": None,
                "deadline": "July 31",
            }
        ],
        "eligibility_requirements": [
            {
                "requirement": "Applicant must be at least 18.",
                "evidence": "Applicants must be 18 years or older.",
            }
        ],
        "important_deadlines": [
            {
                "description": "Application deadline",
                "date": "July 31",
                "source_text": "Applications must be submitted by July 31.",
            }
        ],
        "required_documents": ["Government-issued identification"],
        "risks": [
            {
                "description": "Late applications may be rejected.",
                "severity": "high",
                "mitigation": "Submit before the stated deadline.",
            }
        ],
        "recommended_next_steps": [
            "Confirm eligibility.",
            "Collect the required identification.",
        ],
    }


def test_document_analysis_accepts_valid_structured_data() -> None:
    analysis = DocumentAnalysis.model_validate(valid_analysis_data())

    assert analysis.executive_summary == (
        "The program provides workforce training."
    )
    assert analysis.key_action_items[0].priority == "high"
    assert len(analysis.required_documents) == 1


def test_document_analysis_rejects_unknown_fields() -> None:
    data = valid_analysis_data()
    data["unsupported_field"] = "unexpected"

    with pytest.raises(ValidationError):
        DocumentAnalysis.model_validate(data)


def test_document_analysis_rejects_invalid_priority() -> None:
    data = valid_analysis_data()
    data["key_action_items"][0]["priority"] = "urgent"

    with pytest.raises(ValidationError):
        DocumentAnalysis.model_validate(data)


def test_document_analysis_rejects_empty_summary() -> None:
    data = valid_analysis_data()
    data["executive_summary"] = ""

    with pytest.raises(ValidationError):
        DocumentAnalysis.model_validate(data)


def test_document_analysis_defaults_optional_lists() -> None:
    analysis = DocumentAnalysis(
        executive_summary="A valid summary."
    )

    assert analysis.key_action_items == []
    assert analysis.eligibility_requirements == []
    assert analysis.important_deadlines == []
    assert analysis.required_documents == []
    assert analysis.risks == []
    assert analysis.recommended_next_steps == []