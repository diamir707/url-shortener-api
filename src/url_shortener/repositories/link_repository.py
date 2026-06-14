from typing import Protocol

from url_shortener.models.link import Link


class LinkRepository(Protocol):
    def create_link(self, link: Link) -> Link:
        """Store a new link and return it."""

    def get_link(self, short_code: str) -> Link | None:
        """Return a link by short code, or None if it does not exist."""

    def delete_link(self, short_code: str) -> None:
        """Delete a link by short code."""

    def increment_click_count(self, short_code: str) -> None:
        """Increase click count for a link."""