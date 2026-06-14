import pytest

from url_shortener.shared.errors import ValidationError
from url_shortener.shared.validation import validate_target_url


@pytest.mark.parametrize(
    "url",
    [
        "https://example.com",
        "http://example.com/path?campaign=test",
        "https://sub.example.com/a/b#section"
    ]
)
def test_validate_target_url_accepts_http_and_https_urls(url: str) -> None:
    assert validate_target_url(url) == url

@pytest.mark.parametrize(
    "url",
    [
        "",
        "example.com",
        "ftp://example.com",
        "https://",
        "mailto:test@example.com"
    ]
)
def test_validate_target_url_rejects_invalid_urls(url: str) -> None:
    with pytest.raises(ValidationError):
        validate_target_url(url)