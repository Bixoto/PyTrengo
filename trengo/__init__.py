import os
from collections.abc import Iterator
from datetime import datetime
from typing import Any, Iterable

from api_session import APISession, JSONDict, escape_path

__all__ = ["Trengo", "__version__"]
__version__ = "0.1.0"


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
    # == WhatsApp ==
    # == Contacts ==

    def get_contacts(self, term: str | None, **kwargs):
        """Yield all contacts."""
        return self._get_paginated("/contacts",
                                   params={"term": term},
                                   **kwargs)

    # == Profiles ==

    def get_profiles(self, term: str | None, **kwargs):
        """Yield all profiles."""
        return self._get_paginated("/profiles",
                                   params={"term": term},
                                   **kwargs)

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

    def get_webhook(self, webhook_id: int, **kwargs):
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
            value = value.replace(microsecond=0).isoformat()
        elif isinstance(value, bool):
            value = "true" if value else "false"

        formatted_params[name] = value

    return formatted_params
