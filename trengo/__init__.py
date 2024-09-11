import os
from collections.abc import Iterator
from typing import Any

from api_session import APISession, JSONDict
from dotenv import load_dotenv

load_dotenv()


class Trengo(APISession):
    def __init__(self, token: str | None = None):
        if token is None:
            token = os.environ.get("TRENGO_TOKEN")
            if token is None:
                raise RuntimeError("No Trengo token provided, and the environment variable TRENGO_TOKEN is not set")

        super().__init__(
            base_url="https://app.trengo.eu/api/v2",
        )
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

    def get_users(self, **kwargs):
        """Yield all users."""
        return self._get_paginated("/users", **kwargs)

    def get_labels(self, **kwargs):
        """Yield all labels."""
        return self._get_paginated("/labels", **kwargs)
