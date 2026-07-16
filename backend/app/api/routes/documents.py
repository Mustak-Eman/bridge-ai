from typing import Annotated

from fastapi import APIRouter, File, UploadFile, status

from app.api.dependencies.documents import (
    DocumentAnalysisServiceDependency,
)
from app.schemas.document_analysis import (
    AIAnalysisMetadataResponse,
    DocumentAnalysisResponse,
    DocumentMetadataResponse,
)


router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)


@router.post(
    "/analyze",
    response_model=DocumentAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze an operational document",
    description=(
        "Upload a PDF, TXT, or Markdown document and receive a "
        "structured operational analysis."
    ),
)
async def analyze_document(
    service: DocumentAnalysisServiceDependency,
    file: Annotated[
        UploadFile,
        File(
            description=(
                "A PDF, TXT, or Markdown document to analyze."
            )
        ),
    ],
) -> DocumentAnalysisResponse:
    content = await file.read()

    result = await service.analyze_document(
        filename=file.filename,
        media_type=file.content_type,
        content=content,
    )

    return DocumentAnalysisResponse(
        document=DocumentMetadataResponse(
            filename=file.filename or "unknown",
            media_type=(
                file.content_type
                or "application/octet-stream"
            ),
            size_bytes=len(content),
        ),
        analysis=result.analysis,
        metadata=AIAnalysisMetadataResponse(
            prompt_name=result.metadata.prompt_name,
            prompt_version=result.metadata.prompt_version,
            provider=result.metadata.provider,
            model=result.metadata.model,
        ),
    )