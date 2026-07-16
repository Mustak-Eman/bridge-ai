from pydantic import BaseModel, ConfigDict, Field


class ValidatedDocument(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
    )

    filename: str = Field(min_length=1)
    extension: str = Field(min_length=1)
    media_type: str = Field(min_length=1)
    content: bytes
    size_bytes: int = Field(ge=1)


class ParsedDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")

    filename: str = Field(min_length=1)
    extension: str = Field(min_length=1)
    media_type: str = Field(min_length=1)
    text: str = Field(min_length=1)
    size_bytes: int = Field(ge=1)
    character_count: int = Field(ge=1)
    page_count: int | None = Field(default=None, ge=1)
    title: str | None = None