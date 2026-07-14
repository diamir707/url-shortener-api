from typing import Any

from url_shortener.shared.config import get_config
from url_shortener.shared.dependencies import get_link_service
from url_shortener.shared.errors import ValidationError
from url_shortener.shared.logger import get_logger
from url_shortener.shared.requests import parse_json_body
from url_shortener.shared.response import error_response, json_response
from url_shortener.shared.validation import parse_optional_expires_at

logger = get_logger(__name__)


def handler(event: dict[str, Any], context: object) -> dict[str, Any]:
    try:
        body = parse_json_body(event)

        target_url = body.get("targetUrl")
        expires_at = parse_optional_expires_at(body.get("expiresAt"))

        service = get_link_service()
        config = get_config()

        link = service.create_link(
            target_url=target_url,
            expires_at=expires_at,
        )
        
        logger.info("Created short link: %s", link.short_code)

        return json_response(
            status_code=201,
            body={
                "shortCode": link.short_code,
                "shortUrl": f"{config.base_url}/{link.short_code}",
                "targetUrl": link.target_url,
                "expiresAt": (
                    link.expires_at.isoformat()
                    if link.expires_at is not None
                    else None
                ),
            },
        )

    except ValidationError as exc:
        logger.info("Validation error while creating link: %s", exc)
        return error_response(400, str(exc))

    except Exception:
        logger.exception("Unexpected error while creating link")
        return error_response(500, "Internal server error")