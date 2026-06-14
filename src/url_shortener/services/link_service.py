import secrets
import string
from datetime import UTC, datetime
from typing import Final

from url_shortener.models.link import Link
from url_shortener.repositories.link_repository import LinkRepository
from url_shortener.shared.errors import DuplicateShortCodeError, LinkExpiredError, LinkNotFoundError
from url_shortener.shared.validation import validate_target_url

DEFAULT_SHORT_CODE_LENGTH: Final[int] = 7
SHORT_CODE_ALPHABET: Final[str] = string.ascii_letters + string.digits


class LinkService:
    def __init__(
        self,
        repository: LinkRepository,
        *,
        short_code_length: int = DEFAULT_SHORT_CODE_LENGTH
    ) -> None:
        self._repository = repository
        self.short_code_length = short_code_length

    def create_link(
        self,
        *,
        target_url: str,
        expires_at: datetime | None
    ) -> Link:
        validated_target_url = validate_target_url(target_url)
        short_code = self._generate_unique_short_code()
        created_at = datetime.now(UTC)
        ttl = self._to_ttl(expires_at)

        link = Link(
            short_code=short_code,
            target_url=validated_target_url,
            created_at=created_at,
            expires_at=expires_at,
            ttl=ttl,
            click_count=0
        )

        return self._repository.create_link(link)
    
    def resolve_redirect(self, short_code: str) -> str:
        link = self._repository.get_link(short_code)

        if link is None:
            raise LinkNotFoundError(f"Link not found: {short_code}")
        
        if link.is_expired:
            raise LinkExpiredError(f"Link has expired: {short_code}")
        
        self._repository.increment_click_count(short_code)

        return link.target_url
    
    def get_link(self, short_code: str) -> Link:
        link = self._repository.get_link(short_code)

        if link is None:
            raise LinkNotFoundError(f"Link not found: {short_code}")
        
        return link
    
    def delete_link(self, short_code: str) -> None:
        link = self._repository.get_link(short_code)

        if link is None:
            raise LinkNotFoundError(f"Link not found: {short_code}")
        
        self._repository.delete_link(short_code)

    def _generate_unique_short_code(self) -> str:
        for _ in range(5):
            short_code = self._generate_short_code()

        if self._repository.get_link(short_code) is None:
            return short_code
        
        raise DuplicateShortCodeError("Could not generate a unique short code")
    
    def _generate_short_code(self) -> str:
        return "".join(
            secrets.choice(SHORT_CODE_ALPHABET)
            for _ in range(self.short_code_length)
        )
    
    @staticmethod
    def _to_ttl(expires_at: datetime | None) -> int | None:
        if expires_at is None:
            return None
        
        return int(expires_at.timestamp())