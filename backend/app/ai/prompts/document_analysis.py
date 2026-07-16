from app.ai.prompts.base import PromptDefinition
from app.documents.models import ParsedDocument


DOCUMENT_ANALYSIS_PROMPT_NAME = "document_operational_analysis"
DOCUMENT_ANALYSIS_PROMPT_VERSION = "1.0"


SYSTEM_PROMPT = """
You analyze operational documents for community organizations.

Return only information supported by the provided document.

Do not invent:
- eligibility rules
- deadlines
- required documents
- risks
- action items
- next steps

When information is missing or unclear, omit it or use a null value where
the response schema permits null.

Focus on operational usefulness. Extract information that helps staff
understand what the document requires, what actions should be taken, and
what risks or deadlines require attention.

The response must conform exactly to the provided structured schema.
""".strip()


def build_document_analysis_user_prompt(
    *,
    document: ParsedDocument,
) -> str:
    title = document.title or "Not provided"

    return (
        "Analyze the following document and produce a structured "
        "operational analysis.\n\n"
        "Document metadata:\n"
        f"- Filename: {document.filename}\n"
        f"- Media type: {document.media_type}\n"
        f"- Title: {title}\n"
        f"- Character count: {document.character_count}\n"
        f"- Page count: {document.page_count or 'Not applicable'}\n\n"
        "Document content:\n"
        "----- BEGIN DOCUMENT -----\n"
        f"{document.text}\n"
        "----- END DOCUMENT -----"
    )


DOCUMENT_ANALYSIS_PROMPT = PromptDefinition(
    name=DOCUMENT_ANALYSIS_PROMPT_NAME,
    version=DOCUMENT_ANALYSIS_PROMPT_VERSION,
    system_prompt=SYSTEM_PROMPT,
    build_user_prompt=build_document_analysis_user_prompt,
)