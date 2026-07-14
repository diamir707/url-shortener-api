from typing import Any

from url_shortener.shared.dependencies import get_link_service
from url_shortener.shared.errors import LinkExpiredError, LinkNotFoundError
from url_shortener.shared.logger import get_logger
from url_shortener.shared.response import error_response, redirect_response

logger = get_logger(__name__)


def handler(event: dict[str, Any], context: object) -> dict[str, Any]:
    try:
        path_parameters = event.get("pathParameters") or {}
        short_code = path_parameters.get("shortCode")

        if not short_code:
            return error_response(400, "shortCode path parameter is required")

        service = get_link_service()
        target_url = service.resolve_redirect(short_code)

        logger.info("Resolved short link: %s", short_code)

        return redirect_response(target_url)

    except LinkNotFoundError as exc:
        logger.info("Short link not found: %s", exc)
        return error_response(404, "Link not found")

    except LinkExpiredError as exc:
        logger.info("Short link expired: %s", exc)
        return error_response(410, "Link expired")

    except Exception:
        logger.exception("Unexpected error while redirecting link")
        return error_response(500, "Internal server error")