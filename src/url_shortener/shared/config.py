import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    base_url: str
    links_table_name: str | None


def get_config() -> Config:
    return Config(
        base_url=os.environ.get("BASE_URL", "http://localhost:3000"),
        links_table_name=os.environ.get("LINKS_TABLE_NAME")
    )