from urllib.parse import urlparse

from url_shortener.shared.errors import ValidationError


def validate_target_url(value: str) -> str:
    if not value or not isinstance(value, str):
        raise ValidationError("targetURL is required")
    
    parsed = urlparse(value)

    if parsed.scheme not in ("http", "https"):
        raise ValidationError("targetURL must start with http:// or https://")
    
    if not parsed.netloc:
        raise ValidationError("targetURL must include a host")
    
    return value

