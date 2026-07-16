from pydantic import BaseModel, ConfigDict, Field

from app.ai.models import DocumentAnalysis


class DocumentMetadataResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    filename: str = Field(min_length=1)
    media_type: str = Field(min_length=1)
    size_bytes: int = Field(ge=1)


class AIAnalysisMetadataResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prompt_name: str = Field(min_length=1)
    prompt_version: str = Field(min_length=1)
    provider: str = Field(min_length=1)
    model: str = Field(min_length=1)


class DocumentAnalysisResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    document: DocumentMetadataResponse
    analysis: DocumentAnalysis
    metadata: AIAnalysisMetadataResponse