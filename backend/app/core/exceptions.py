class AppException(Exception):
    """Base application exception."""
    
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundException(AppException):
    """Exception raised when a requested resource is not found."""
    
    def __init__(self, resource: str, resource_id: int):
        self.resource = resource
        self.resource_id = resource_id
        super().__init__(
            message=f"{resource} with id {resource_id} not found",
            status_code=404
        )


class DeletionNotAllowedException(AppException):
    """Exception raised when a resource cannot be deleted. """
    
    def __init__(self, resource: str, reason: str):
        self.resource = resource
        self.reason = reason
        super().__init__(
            message=f"Cannot delete {resource}: {reason}",
            status_code=400
        )


class ValidationException(AppException):
    """Exception raised when validation fails."""
    
    def __init__(self, message: str):
        super().__init__(message=message, status_code=400)
