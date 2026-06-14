from datetime import UTC, datetime, timedelta

import pytest

from url_shortener.models.link import Link
from url_shortener.services.link_service import LinkService
from url_shortener.shared.errors import LinkExpiredError, LinkNotFoundError, ValidationError


class InMemoryLinkRepository:
    def __init__(self) -> None:
        self.links: dict[str, Link] = {}

    def create_link(self, link: Link) -> Link:
        self.links[link.short_code] = link
        return link
    
    def get_link(self, short_code: str) -> Link | None:
        return self.links.get(short_code)

    def delete_link(self, short_code: str) -> None:
        self.links.pop(short_code, None)

    def increment_click_count(self, short_code: str) -> None:
        link = self.links[short_code]
        self.links[short_code] = Link(
            short_code=link.short_code,
            target_url=link.target_url,
            created_at=link.created_at,
            expires_at=link.expires_at,
            ttl=link.ttl,
            click_count=link.click_count + 1,
        )


def test_create_link_stores_valid_link() -> None:
    repository = InMemoryLinkRepository()
    service = LinkService(repository)

    link = service.create_link(target_url="https://example.com", expires_at=None)
    
    assert link.short_code
    assert link.target_url == "https://example.com"
    assert link.click_count == 0
    assert repository.get_link(link.short_code) == link


def test_create_link_rejects_invalid_url() -> None:
    repository = InMemoryLinkRepository()
    service = LinkService(repository)
    
    with pytest.raises(ValidationError):
        service.create_link(target_url="not-a-url", expires_at=None)


def test_create_link_with_expiration_sets_ttl() -> None:
    repository = InMemoryLinkRepository()
    service = LinkService(repository)
    
    expires_at = datetime.now(UTC) + timedelta(days=1)

    link = service.create_link(
        target_url="https://example.com",
        expires_at=expires_at,
    )

    assert link.expires_at == expires_at
    assert link.ttl == int(expires_at.timestamp())


def test_resolve_redirect_returns_target_url() -> None:
    repository = InMemoryLinkRepository()
    service = LinkService(repository)

    link = service.create_link(target_url="https://example.com", expires_at=None)
    
    target_url = service.resolve_redirect(link.short_code)

    assert target_url == "https://example.com"


def test_resolve_redirect_increments_click_count() -> None:
    repository = InMemoryLinkRepository()
    service = LinkService(repository)
    
    link = service.create_link(target_url="https://example.com", expires_at=None)

    service.resolve_redirect(link.short_code)

    stored_link = repository.get_link(link.short_code)
    
    assert stored_link is not None
    assert stored_link.click_count == 1


def test_resolve_redirect_raises_not_found_for_unknown_code() -> None:
    repository = InMemoryLinkRepository()
    service = LinkService(repository)

    with pytest.raises(LinkNotFoundError):
        service.resolve_redirect("missing")


def test_resolve_redirect_raises_expired_for_expired_link() -> None:
    repository = InMemoryLinkRepository()
    service = LinkService(repository)

    expires_at = datetime.now(UTC) - timedelta(minutes=1)

    link = service.create_link(
        target_url="https://example.com",
        expires_at=expires_at,
    )

    with pytest.raises(LinkExpiredError):
        service.resolve_redirect(link.short_code)


def test_get_link_returns_existing_link() -> None:
    repository = InMemoryLinkRepository()
    service = LinkService(repository)

    created_link = service.create_link(target_url="https://example.com", expires_at=None)

    found_link = service.get_link(created_link.short_code)

    assert found_link == created_link


def test_get_link_raises_not_found_for_unknown_code() -> None:
    repository = InMemoryLinkRepository()
    service = LinkService(repository)

    with pytest.raises(LinkNotFoundError):
        service.get_link("missing")


def test_delete_link_removes_existing_link() -> None:
    repository = InMemoryLinkRepository()
    service = LinkService(repository)

    link = service.create_link(target_url="https://example.com", expires_at=None)

    service.delete_link(link.short_code)
    
    assert repository.get_link(link.short_code) is None


def test_delete_link_raises_not_found_for_unknown_code() -> None:
    repository = InMemoryLinkRepository()
    service = LinkService(repository)

    with pytest.raises(LinkNotFoundError):
        service.delete_link("missing")