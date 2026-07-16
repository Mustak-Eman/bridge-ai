class AppException(Exception):
    """Base exception for expected application-level failures."""

    error_code = "application_error"

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class ResourceNotFoundError(AppException):
    error_code = "resource_not_found"


class ResourceConflictError(AppException):
    error_code = "resource_conflict"


class InvalidOperationError(AppException):
    error_code = "invalid_operation"


class WorkspaceNotFoundError(ResourceNotFoundError):
    error_code = "workspace_not_found"

    def __init__(self) -> None:
        super().__init__("Workspace not found.")


class WorkspaceSlugConflictError(ResourceConflictError):
    error_code = "workspace_slug_conflict"

    def __init__(self, slug: str) -> None:
        super().__init__(
            f"A workspace with slug '{slug}' already exists."
        )


class ProjectNotFoundError(ResourceNotFoundError):
    error_code = "project_not_found"

    def __init__(self) -> None:
        super().__init__("Project not found.")

class ProjectWorkspaceMismatchError(InvalidOperationError):
    error_code = "project_workspace_mismatch"

    def __init__(self) -> None:
        super().__init__(
            "The project does not belong to the specified workspace."
        )

class DocumentValidationError(AppException):
    error_code = "document_validation_error"

    def __init__(self, message: str) -> None:
        super().__init__(message)

class DocumentContentTooLargeError(DocumentValidationError):
    error_code = "document_content_too_large"

class UnsupportedDocumentTypeError(DocumentValidationError):
    error_code = "unsupported_document_type"


class DocumentTooLargeError(DocumentValidationError):
    error_code = "document_too_large"


class EmptyDocumentError(DocumentValidationError):
    error_code = "empty_document"


class DocumentParsingError(AppException):
    error_code = "document_parsing_error"

    def __init__(self, message: str) -> None:
        super().__init__(message)


class DocumentEncodingError(DocumentParsingError):
    error_code = "document_encoding_error"  

class EncryptedDocumentError(DocumentParsingError):
    error_code = "encrypted_document"


class DocumentTextUnavailableError(DocumentParsingError):
    error_code = "document_text_unavailable"    
    
class AIProviderError(AppException):
    error_code = "ai_provider_error"


class AIProviderConfigurationError(AIProviderError):
    error_code = "ai_provider_configuration_error"


class AIProviderUnavailableError(AIProviderError):
    error_code = "ai_provider_unavailable"


class AIStructuredOutputError(AIProviderError):
    error_code = "ai_structured_output_error"
    
