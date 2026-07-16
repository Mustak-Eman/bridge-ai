from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


Priority = Literal["low", "medium", "high"]


class ActionItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: str = Field(min_length=1)
    priority: Priority
    owner: str | None = None
    deadline: str | None = None


class EligibilityRequirement(BaseModel):
    model_config = ConfigDict(extra="forbid")

    requirement: str = Field(min_length=1)
    evidence: str | None = None


class ImportantDeadline(BaseModel):
    model_config = ConfigDict(extra="forbid")

    description: str = Field(min_length=1)
    date: str | None = None
    source_text: str | None = None


class AnalysisRisk(BaseModel):
    model_config = ConfigDict(extra="forbid")

    description: str = Field(min_length=1)
    severity: Priority
    mitigation: str | None = None


class DocumentAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    executive_summary: str = Field(min_length=1)
    key_action_items: list[ActionItem] = Field(default_factory=list)
    eligibility_requirements: list[EligibilityRequirement] = Field(
        default_factory=list
    )
    important_deadlines: list[ImportantDeadline] = Field(default_factory=list)
    required_documents: list[str] = Field(default_factory=list)
    risks: list[AnalysisRisk] = Field(default_factory=list)
    recommended_next_steps: list[str] = Field(default_factory=list)

class AIAnalysisMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prompt_name: str = Field(min_length=1)
    prompt_version: str = Field(min_length=1)
    provider: str = Field(min_length=1)
    model: str = Field(min_length=1)


class DocumentAnalysisResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    analysis: DocumentAnalysis
    metadata: AIAnalysisMetadata