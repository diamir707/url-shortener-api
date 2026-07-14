import json

from url_shortener.handlers.create_link import handler as create_link_handler
from url_shortener.handlers.redirect_link import handler as redirect_link_handler


def test_create_link_handler_returns_201() -> None:
    event = {
        "body": json.dumps(
            {
                "targetUrl": "https://example.com",
            }
        )
    }

    response = create_link_handler(event, None)

    body = json.loads(response["body"])

    assert response["statusCode"] == 201
    assert body["shortCode"]
    assert body["shortUrl"].endswith(f"/{body['shortCode']}")
    assert body["targetUrl"] == "https://example.com"


def test_create_link_handler_returns_400_for_invalid_body() -> None:
    event = {
        "body": json.dumps(
            {
                "targetUrl": "not-a-url",
            }
        )
    }

    response = create_link_handler(event, None)

    assert response["statusCode"] == 400


def test_redirect_link_handler_returns_302_for_existing_link() -> None:
    create_event = {
        "body": json.dumps(
            {
                "targetUrl": "https://example.com",
            }
        )
    }

    create_response = create_link_handler(create_event, None)
    create_body = json.loads(create_response["body"])

    redirect_event = {
        "pathParameters": {
            "shortCode": create_body["shortCode"],
        }
    }

    redirect_response = redirect_link_handler(redirect_event, None)

    assert redirect_response["statusCode"] == 302
    assert redirect_response["headers"]["Location"] == "https://example.com"


def test_redirect_link_handler_returns_404_for_unknown_link() -> None:
    event = {
        "pathParameters": {
            "shortCode": "missing",
        }
    }

    response = redirect_link_handler(event, None)

    assert response["statusCode"] == 404


def test_redirect_link_handler_returns_400_without_short_code() -> None:
    event = {
        "pathParameters": {}
    }

    response = redirect_link_handler(event, None)

    assert response["statusCode"] == 400
