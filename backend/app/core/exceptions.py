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