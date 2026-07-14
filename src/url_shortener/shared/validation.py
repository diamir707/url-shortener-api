from datetime import datetime
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


def parse_optional_expires_at(value: object) -> datetime | None:
    if value is None:
        return None
    
    if not isinstance(value, str):
        raise ValueError("expiresAt must be an ISO-8601 string")
    
    normalized_value = value.replace("Z", "+00:00")

    try:
        return datetime.fromisoformat(normalized_value)
    except ValueError as exc:
        raise ValidationError("expiresAt must be a valid ISO-8601 datetime") from exc
    
    