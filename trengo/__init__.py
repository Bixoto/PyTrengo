import os
from collections.abc import Iterator
from datetime import datetime, timezone
from typing import Any, Iterable

from api_session import APISession, JSONDict, escape_path

__all__ = ["Trengo", "__version__"]
__version__ = "0.1.4"


class Trengo(APISession):
    def __init__(self, *, token: str | None = None, base_url="https://app.trengo.eu/api/v2", **kwargs):
        if token is None:
            token = os.environ.get("TRENGO_TOKEN")
            if token is None:
                raise RuntimeError("No Trengo token provided, and the environment variable TRENGO_TOKEN is not set")

        super().__init__(base_url=base_url, **kwargs)
        self.headers["Authorization"] = f"Bearer {token}"

    def _get_paginated(self, endpoint: str, params: dict[str, Any] | None = None, **kwargs) -> Iterator[JSONDict]:
        if params is None:
            params = {}

        page = 1
        last_page: int | None = None
        while last_page is None or page <= last_page:
            payload = self.get_json_api(endpoint, params={**params, "page": page}, **kwargs)
            yield from payload["data"]

            last_page = payload["meta"]["last_page"]
            page += 1

    # == Tickets ==

    def get_tickets(
            self, *,
            status: str | None = None,
            contact_id: int | None = None,
            users: list[int] | None = None,
            channels: list[int] | None = None,
            last_message_type: str | None = None,
            sort: str | None = None,
            **kwargs,
    ):
        return self._get_paginated(
            "/tickets",
            params=make_params({
                "status": status,
                "contact_id": contact_id,
                "users[]": users,
                "channels[]": channels,
                "last_message_type": last_message_type,
                "sort": sort,
            }),
            **kwargs,
        )

    def get_ticket_aggregates(self, **kwargs) -> dict[str, dict[str, int]]:
        """List all ticket aggregates."""
        return self.get_json_api("/ticket_aggregates", **kwargs)

    def create_ticket(
            self, *,
            channel_id: int,
            contact_id: str,
            subject: str | None = None,
            **kwargs,
    ):
        """Create a ticket."""
        return self.post_json_api(
            "/tickets",
            json={
                "channel_id": channel_id,
                "contact_id": contact_id,
                "subject": subject,
            },
            **kwargs,
        )

    def assign_ticket(
            self, ticket_id: str, *,
            type_: str,
            user_id: int | None = None,
            team_id: int | None = None,
            note: str | None = None,
            **kwargs,
    ):
        """
        Assign a ticket. See also the convenient aliases `assign_ticket_to_user` and `assign_ticket_to_team`.

        :param ticket_id:
        :param type_: This must be `team` or `user`.
        :param user_id:
        :param team_id:
        :param note:
        :param kwargs:
        :return:
        """
        return self.post_json_api(
            f"/tickets/{escape_path(ticket_id)}/assign",
            json={
                "type": type_,
                "user_id": user_id,
                "team_id": team_id,
                "note": note,
            },
            **kwargs,
        )

    def assign_ticket_to_user(self, ticket_id: str, user_id: int, *, note: str | None = None, **kwargs):
        """Alias for `assign_ticket(ticket_id, type_="user", user_id=user_id)."""
        return self.assign_ticket(
            ticket_id=ticket_id,
            type_="user",
            user_id=user_id,
            note=note,
            **kwargs,
        )

    def assign_ticket_to_team(self, ticket_id: str, team_id: int, *, note: str | None = None, **kwargs):
        """Alias for `assign_ticket(ticket_id, type_="team", team_id=team_id)."""
        return self.assign_ticket(
            ticket_id=ticket_id,
            type_="team",
            team_id=team_id,
            note=note,
            **kwargs,
        )

    def close_ticket(self, ticket_id: int, *, ticket_result_id: int | None = None, **kwargs):
        """Close a ticket."""
        return self.post_json_api(
            f"/tickets/{escape_path(ticket_id)}/close",
            json={
                "ticket_id": ticket_id,
                "ticket_result_id": ticket_result_id,
            },
            **kwargs,
        )

    def reopen_ticket(self, ticket_id: int, **kwargs):
        """Reopen a ticket."""
        return self.post_json_api(
            f"/tickets/{escape_path(ticket_id)}/reopen",
            json={},
            **kwargs,
        )

    def merge_ticket(self, source_ticket_id: int, target_ticket_id: int, **kwargs):
        """Merge a ticket."""
        return self.post_json_api(
            f"/tickets/{escape_path(target_ticket_id)}/merge",
            json={
                "source_ticket_id": source_ticket_id,
            },
            **kwargs,
        )

    def attach_ticket_label(self, ticket_id: int, label_id: int, **kwargs):
        """Attach a label to a ticket."""
        return self.post_json_api(
            f"/tickets/{escape_path(ticket_id)}/labels",
            json={"label_id": label_id},
            **kwargs,
        )

    def detach_ticket_label(self, ticket_id: int, label_id: int, **kwargs):
        """Detach a label from a ticket."""
        return self.delete_json_api(
            f"/tickets/{escape_path(ticket_id)}/labels/{escape_path(label_id)}",
            **kwargs,
        )

    def delete_ticket(self, ticket_id: int, **kwargs):
        """Delete a ticket."""
        return self.delete_json_api(
            f"/tickets/{escape_path(ticket_id)}",
            **kwargs,
        )

    def mark_ticket_as_spam(self, ticket_id: int, **kwargs):
        """Mark a ticket as spam"""
        return self.post_json_api(f"/tickets/{escape_path(ticket_id)}/spam", **kwargs)

    def unmark_ticket_as_spam(self, ticket_id: int, **kwargs):
        """Unmark a ticket as spam"""
        return self.delete_json_api(f"/tickets/{escape_path(ticket_id)}/spam", **kwargs)

    def set_custom_data(self, ticket_id: int, custom_field_id: int, value: str, **kwargs):
        """Set a custom field value for a ticket."""
        return self.post_json_api(f"/tickets/{escape_path(ticket_id)}/custom_fields",
                                  json={"custom_field_id": custom_field_id, "value": value},
                                  **kwargs)

    def delete_message(self, ticket_id: int, message_id: int, **kwargs):
        """Delete a message."""
        return self.delete_json_api(f"/{escape_path(ticket_id)}/messages/{escape_path(message_id)}",
                                    **kwargs)

    def send_ticket_message(self, ticket_id: int, message: str, *,
                            is_internal_note: bool | None = None,
                            subject: str | None = None,
                            attachments_ids: Iterable[int] | None = None,
                            **kwargs):
        """Send a ticket message."""
        return self.post_json_api(
            f"/tickets/{escape_path(ticket_id)}/messages",
            json={
                "message": message,
                "internal_note": is_internal_note,
                "subject": subject,
                "attachments_ids": list(attachments_ids) if attachments_ids else None,
            },
            **kwargs
        )

    def send_ticket_media_message(self, ticket_id: str, *,
                                  file: str,
                                  caption: str | None = None,
                                  **kwargs):
        """
        Send a ticket media message (UNTESTED).
        """
        return self.post_json_api(
            f"/tickets/{escape_path(ticket_id)}/messages/media",
            json={
                "file": file,
                "caption": caption,
            },
            **kwargs,
        )

    def get_messages(self, ticket_id: int, **kwargs):
        """Yield all messages from a ticket."""
        return self._get_paginated(f"/tickets/{escape_path(ticket_id)}/messages", **kwargs)

    def mark_ticket_as_favorite(self, ticket_id: int, **kwargs):
        """Mark a ticket as favorite"""
        return self.post_json_api(f"/tickets/{escape_path(ticket_id)}/favorited", **kwargs)

    def unmark_ticket_as_favorite(self, ticket_id: int, **kwargs):
        """Unmark a ticket as favorite"""
        return self.delete_json_api(f"/tickets/{escape_path(ticket_id)}/favorited/0", **kwargs)

    def get_message(self, ticket_id: int, message_id: int, **kwargs) -> JSONDict | None:
        """Get a single message."""
        return self.get_json_api(f"/tickets/{escape_path(ticket_id)}/messages/{escape_path(message_id)}", **kwargs)

    def store_custom_channel_message(self, channel: str, *,
                                     contact: dict[str, Any] | None = None,
                                     text: str,
                                     attachments: Iterable[dict[str, Any]] | None = None,
                                     **kwargs):
        """Store a custom channel message (UNTESTED)."""
        return self.post_json_api(
            "/v2/custom_channel_messages",
            json={
                "channel": channel,
                "contact": contact,
                "body": {"text": text},
                "attachments": list(attachments) if attachments else None,
            },
            **kwargs,
        )

    # == WhatsApp ==

    def send_whatsapp_template(
            self,
            recipient_phone_number: str, *,
            hsm_id: int,
            params: list[JSONDict] | None = None,
            ticket_id: str | None = None,
            source: str | None = None,
            **kwargs,
    ):
        """Send a WhatsApp template."""
        return self.post_json_api(
            "/wa_sessions",
            json={
                "recipient_phone_number": recipient_phone_number,
                "hsm_id": hsm_id,
                "params": params or [],
                "ticket_id": ticket_id,
                "source": source,
            },
            **kwargs,
        )

    # == Contacts ==

    def get_contacts(self, term: str | None = None, **kwargs):
        """Yield all contacts."""
        return self._get_paginated("/contacts",
                                   params={"term": term},
                                   **kwargs)

    def get_contact(self, contact_id: int, include: list[str] | None = None, **kwargs) -> JSONDict | None:
        """
        Get a single contact.

        :param contact_id:
        :param include: Eager load relations (available: "notes")
        :return:
        """
        return self.get_json_api(
            f"/contacts/{escape_path(contact_id)}",
            params={"include": ",".join(include) if include else None},
            **kwargs,
        )

    def create_contact(self, channel_id: int, identifier: str, *, full_name: str | None = None, **kwargs) -> JSONDict:
        """
        Create a contact if it doesn't exist, and return it.
        """
        return self.post_json_api(
            f"/channels/{escape_path(channel_id)}/contacts",
            json={
                "identifier": identifier,
                "channel_id": channel_id,
                "name": full_name,
            },
            **kwargs,
        )

    def update_contact(self, contact_id: int, *, full_name: str | None = None, contact_group_ids: list[int] | None,
                       **kwargs):
        """Update a contact."""
        return self.put_json_api(
            f"/contacts/{contact_id}",
            json={
                "name": full_name,
                "contact_group_ids": contact_group_ids,
            },
            **kwargs,
        )

    # == Profiles ==

    def get_profiles(self, term: str | None = None, **kwargs):
        """Yield all profiles."""
        return self._get_paginated("/profiles",
                                   params={"term": term},
                                   **kwargs)

    def get_profile(self, profile_id: int, include: list[str] | None = None, **kwargs) -> JSONDict | None:
        """
        Get a single profile.

        :param profile_id:
        :param include: Eager load relations (available: "user", "notes").
          Note using both "user" and "notes" is untested.
        """
        return self.get_json_api(
            f"/profiles/{escape_path(profile_id)}",
            # NOTE: it’s not clear how to combine "user" and "notes" here;
            #   the documentation only seems to allow "user" OR "notes" and the API doesn't enforce the value:
            #   we can use "foo" with no error.
            params={"with": ",".join(include) if include else None},
            **kwargs,
        )

    # == SMS Messages ==

    def get_sms_messages(self, **kwargs):
        """Yield all SMS messages."""
        return self._get_paginated("/sms_messages", **kwargs)

    # == Messages ==
    # == Team Chat ==
    # == VoIP ==
    # == Help Center ==

    def get_help_centers(self, **kwargs):
        """Yield all help centers."""
        # yes it’s "help_center", not "help_centers"
        return self._get_paginated("/help_center", **kwargs)

    def get_help_center_categories(self, help_center_id: int, **kwargs):
        """Yield all help center categories."""
        return self._get_paginated(f"/help_center/{escape_path(help_center_id)}/categories", **kwargs)

    def get_help_center_blocks(self, help_center_id: int, **kwargs):
        """Yield all help center blocks."""
        return self._get_paginated(f"/help_center/{escape_path(help_center_id)}/blocks", **kwargs)

    def get_help_center(self, help_center_id: int, **kwargs) -> JSONDict | None:
        """Get a help center."""
        return self.get_json_api(f"/help_center/{escape_path(help_center_id)}", **kwargs)

    def get_help_center_category(self, help_center_id: int, category_id: int, **kwargs) -> JSONDict | None:
        """Get a help center category."""
        return self.get_json_api(f"/help_center/{escape_path(help_center_id)}/categories/{escape_path(category_id)}",
                                 **kwargs)

    def get_help_center_article(self, help_center_id: int, article_id: int, **kwargs) -> JSONDict | None:
        """Get a help center article."""
        return self.get_json_api(f"/help_center/{escape_path(help_center_id)}/articles/{escape_path(article_id)}",
                                 **kwargs)

    def get_help_center_block(self, help_center_id: int, block_id: int, **kwargs) -> JSONDict | None:
        """Get a help center block."""
        return self.get_json_api(f"/help_center/{escape_path(help_center_id)}/blocks/{escape_path(block_id)}",
                                 **kwargs)

    def delete_help_center(self, help_center_id: int, **kwargs):
        """Delete a help center."""
        return self.delete_json_api(f"/help_center/{escape_path(help_center_id)}", **kwargs)

    def delete_help_center_category(self, help_center_id: int, category_id: int, **kwargs):
        """Delete a help center category."""
        return self.delete_json_api(f"/help_center/{escape_path(help_center_id)}/categories/{escape_path(category_id)}",
                                    **kwargs)

    # == Quick Replies ==

    def get_quick_replies(self, reply_type: str, **kwargs):
        """
        Yield all quick replies.

        :param reply_type: "SMS" (deprecated), "MESSAGING", or "EMAIL".
        """
        return self._get_paginated("/quick_replies",
                                   params={"type": reply_type.upper()},
                                   **kwargs)

    # == Ticket Results ==

    def get_ticket_results(self, **kwargs):
        """Yield all ticket results."""
        return self._get_paginated("/ticket_results", **kwargs)

    # == Contact Groups ==

    def get_contact_groups(self, **kwargs):
        """Yield all contact groups."""
        return self._get_paginated("/contact_groups", **kwargs)

    # == Labels ==

    def get_labels(self, **kwargs):
        """Yield all labels."""
        return self._get_paginated("/labels", **kwargs)

    # == Teams ==

    def get_teams(self, **kwargs):
        """Yield all teams."""
        return self._get_paginated("/teams", **kwargs)

    # == Users ==

    def get_users(self, **kwargs):
        """Yield all users."""
        return self._get_paginated("/users", **kwargs)

    # == Custom Fields ==

    def get_custom_fields(self, **kwargs):
        """Yield all custom fields."""
        return self._get_paginated("/webhcustom_fieldsooks", **kwargs)

    # == Webhooks ==

    def get_webhooks(self, **kwargs):
        """Yield all webhooks."""
        return self._get_paginated("/webhooks", **kwargs)

    def create_webhook(
            self, *,
            name: str,
            type_: str,
            url: str,
            **kwargs,
    ):
        """Create a webhook.

        See https://developers.trengo.com/docs/webhooks.
        """
        return self.post_json_api(
            "/webhooks",
            json={
                "name": name,
                "type": type_,
                "url": url,
            },
            **kwargs
        )

    def get_webhook(self, webhook_id: int, **kwargs) -> JSONDict | None:
        """Get a webhook"""
        return self.get_json_api(f"/webhooks/{escape_path(webhook_id)}", **kwargs)

    # == Quick Actions ==
    # == Beta - Reporting ==

    def get_reporting_metrics(self, metrics: Iterable[str], *,
                              start_date: str | datetime | None = None,
                              end_date: str | datetime | None = None,
                              team_ids: Iterable[int] | None = None,
                              channel_ids: Iterable[int] | None = None,
                              label_ids: Iterable[int] | None = None,
                              direction: str | None = None,
                              **kwargs) -> dict[str, int | float]:
        """
        Get reporting metrics.

        :param metrics: Metrics to retrieve. ``["*"]`` is a convenient alias for
            ``['new_tickets', 'assigned_tickets', 'average_total_resolution_time', 'average_first_response_time',
               'created_tickets', 'closed_tickets', 'reopened_tickets']``, i.e. all the metrics documented.
        :param start_date:
        :param end_date:
        :param team_ids:
        :param channel_ids:
        :param label_ids:
        :param direction:
        :param kwargs:
        :return:
        """
        if metrics == ["*"]:
            metrics = ['new_tickets', 'assigned_tickets', 'average_total_resolution_time',
                       'average_first_response_time', 'created_tickets', 'closed_tickets',
                       'reopened_tickets']

        return self.get_json_api(
            "/reporting/metrics",
            params=make_params({
                "metric[]": metrics,
                "start_date": start_date,
                "end_date": end_date,
                "team_ids[]": team_ids,
                "channel_ids[]": channel_ids,
                "label_ids[]": label_ids,
                "direction": direction,
            }),
            **kwargs,
        )["aggregates"]


def make_params(params: dict[str, Any]):
    formatted_params: dict[str, Any] = {}

    for name, value in params.items():
        if value is None:
            continue

        if name.endswith("[]"):
            value = list(value)
        elif isinstance(value, datetime):
            # Format: 2024-01-01T00:00:00+01:00
            value = value.replace(microsecond=0, tzinfo=value.tzinfo or timezone.utc).isoformat()
        elif isinstance(value, bool):
            value = "true" if value else "false"

        formatted_params[name] = value

    return formatted_params
