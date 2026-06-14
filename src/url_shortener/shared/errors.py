class UrlShortenerError(Exception):
    """Base application error."""


class ValidationError(UrlShortenerError):
    """Raised when user input is invalid."""


class LinkNotFoundError(UrlShortenerError):
    """Raised when a short link does not exist."""


class LinkExpiredError(UrlShortenerError):
    """Raised when a short link exists but is expired."""


class DuplicateShortCodeError(UrlShortenerError):
    """Raised when a generated or requested short code already exists."""