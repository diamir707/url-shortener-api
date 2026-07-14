import json
from typing import Any

from url_shortener.shared.errors import ValidationError


def parse_json_body(event: dict[str, Any]) -> dict[str, Any]:
    raw_body = event.get("body")

    if not raw_body:
        raise ValidationError("Request body is required")
    
    try:
        parsed_body = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValidationError("Request body must be a valid JSON") from exc
    
    if not isinstance(parsed_body, dict):
        raise ValidationError("Request body must be a JSON object")
    
    return parsed_body
