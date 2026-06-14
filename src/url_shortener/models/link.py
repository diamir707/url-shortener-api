from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True)
class Link:
    short_code: str
    target_url: str
    created_at: datetime
    expires_at: datetime | None
    ttl: int | None
    click_count: int = 0

    @property
    def is_expired(self) -> bool:
        return self.expires_at is not None and datetime.now(UTC) >= self.expires_at