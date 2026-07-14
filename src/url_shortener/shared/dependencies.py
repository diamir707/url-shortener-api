from url_shortener.repositories.in_memory_link_repository import InMemoryLinkRepository
from url_shortener.services.link_service import LinkService

_repository = InMemoryLinkRepository()


def get_link_service() -> LinkService:
    return LinkService(_repository)
