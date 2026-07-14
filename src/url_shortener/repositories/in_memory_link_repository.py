from url_shortener.models.link import Link


class InMemoryLinkRepository:
    def __init__(self):
        self._links: dict[str, Link] = {}

    def create_link(self, link: Link) -> Link:
        self._links[link.short_code] = link
        return link

    def get_link(self, short_code: str) -> Link | None:
        return self._links.get(short_code)

    def delete_link(self, short_code: str) -> None:
        self._links.pop(short_code, None)

    def increment_click_count(self, short_code: str) -> None:
        link = self._links[short_code]

        self._links[short_code] = Link(
            short_code=link.short_code,
            target_url=link.target_url,
            created_at=link.created_at,
            expires_at=link.expires_at,
            ttl=link.ttl,
            click_count=link.click_count + 1,
        )
