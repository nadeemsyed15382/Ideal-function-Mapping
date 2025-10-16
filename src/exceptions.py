"""Custom exception types for the IU Python Function Mapping project."""

class DataValidationError(Exception):
    """Raised when CSV content or schema is invalid."""
    pass

class DatabaseError(Exception):
    """Raised for database connection/write issues."""
    pass
