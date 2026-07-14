import json
from typing import Any


def json_response(
    status_code: int,
    body: dict[str, Any],
    headers: dict[str, str] | None = None,
) -> dict[str, Any]:

    response_headers = {
        "Content-Type": "application/json",
    }

    if headers:
        response_headers.update(headers)

    return {
        "statusCode": status_code,
        "headers": response_headers,
        "body": json.dumps(body)
    }


def error_response(status_code: int, message: str) -> dict[str, Any]:
    return json_response(
        status_code=status_code,
        body={
            "error": message
        },
    )


def redirect_response(location: str) -> dict[str, Any]:
    return {
        "statusCode": 302,
        "headers": {
            "Location": location,
        },
        "body": "",
    }
