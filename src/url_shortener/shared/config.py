import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    base_url: str


def get_config() -> Config:
    return Config(
        base_url=os.environ.get("BASE_URL", "http://localhost:3000")
    )