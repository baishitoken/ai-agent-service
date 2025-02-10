class SDKError(Exception):
    """Base class for SDK exceptions."""
    pass

class GameDataProcessingError(SDKError):
    """Raised when there's an error processing game data."""
    pass

class APIClientError(SDKError):
    """Raised when there’s an error with the API client."""
    pass
