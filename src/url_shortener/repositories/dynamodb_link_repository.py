from datetime import UTC, datetime
from typing import Any

import boto3
from botocore.exceptions import ClientError

from url_shortener.models.link import Link
from url_shortener.shared.errors import DuplicateShortCodeError


class DynamoDbLinkRepository:
    def __init__(
        self,
        *,
        table_name: str,
        dynamodb_resource: Any | None = None,
    ) -> None:
        self._table_name = table_name
        self._dynamodb_resource = dynamodb_resource or boto3.resource("dynamodb")
        self._table = self._dynamodb_resource.Table(table_name)

    def create_link(self, link: Link) -> Link:
        try:
            self._table.put_item(
                Item=self._to_item(link),
                ConditionExpression="attribute_not_exists(shortCode)",
            )
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "ConditionalCheckFailedException":
                raise DuplicateShortCodeError(
                    f"Short code already exists: {link.short_code}"
                ) from exc

            raise

        return link

    def get_link(self, short_code: str) -> Link | None:
        response = self._table.get_item(
            Key={
                "shortCode": short_code,
            }
        )

        item = response.get("Item")

        if item is None:
            return None

        return self._from_item(item)

    def delete_link(self, short_code: str) -> None:
        self._table.delete_item(
            Key={
                "shortCode": short_code,
            }
        )

    def increment_click_count(self, short_code: str) -> None:
        self._table.update_item(
            Key={
                "shortCode": short_code,
            },
            UpdateExpression="ADD clickCount :increment",
            ExpressionAttributeValues={
                ":increment": 1,
            },
        )

    @staticmethod
    def _to_item(link: Link) -> dict[str, Any]:
        item: dict[str, Any] = {
            "shortCode": link.short_code,
            "targetUrl": link.target_url,
            "createdAt": link.created_at.isoformat(),
            "clickCount": link.click_count,
        }

        if link.expires_at is not None:
            item["expiresAt"] = link.expires_at.isoformat()

        if link.ttl is not None:
            item["ttl"] = link.ttl

        return item

    @staticmethod
    def _from_item(item: dict[str, Any]) -> Link:
        expires_at_raw = item.get("expiresAt")
        ttl_raw = item.get("ttl")

        return Link(
            short_code=item["shortCode"],
            target_url=item["targetUrl"],
            created_at=datetime.fromisoformat(item["createdAt"]).astimezone(UTC),
            expires_at=(
                datetime.fromisoformat(expires_at_raw).astimezone(UTC)
                if expires_at_raw is not None
                else None
            ),
            ttl=int(ttl_raw) if ttl_raw is not None else None,
            click_count=int(item.get("clickCount", 0)),
        )