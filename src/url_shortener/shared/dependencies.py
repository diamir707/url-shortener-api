from url_shortener.repositories.dynamodb_link_repository import DynamoDbLinkRepository
from url_shortener.repositories.in_memory_link_repository import InMemoryLinkRepository
from url_shortener.services.link_service import LinkService
from url_shortener.shared.config import get_config

_in_memory_repository = InMemoryLinkRepository()
_link_service: LinkService | None = None


def get_link_service() -> LinkService:
    global _link_service

    config = get_config()

    if config.links_table_name is None:
        return LinkService(_in_memory_repository)
    
    if _link_service is None:
        repository = DynamoDbLinkRepository(table_name=config.links_table_name)
        _link_service = LinkService(repository)

    return _link_service
