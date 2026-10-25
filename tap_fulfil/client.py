"""HTTP API client (REST or GraphQL), including FulfilStream base class."""

from __future__ import annotations

from typing import Any

import requests
from hotglue_singer_sdk.authenticators import APIKeyAuthenticator
from hotglue_singer_sdk.streams import RESTStream
from typing_extensions import override


class FulfilStream(RESTStream):
    """Fulfil stream class."""

    # Update this value if necessary or override `parse_response`.
    records_jsonpath = "$[*]"

    page_size = 10

    @override
    @property
    def url_base(self) -> str:
        """Return the API URL root, preserving the connector's ``base_url`` setting."""
        return self.config.get(
            "base_url", self.config.get("api_url", "https://dev.fulfil.io/api/v2")
        ).rstrip("/")

    @override
    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return APIKeyAuthenticator(
            stream=self,
            key="X-API-KEY",
            value=self.config["access_key"],
            location="header",
        )

    @override
    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        return {"Accept": "application/json"}

    def get_next_page_token(
        self,
        response: requests.Response,
        previous_token: Any | None,
    ) -> Any | None:
        """Return token identifying next page or None if all records have been read.

        Args:
            response: A raw `requests.Response`_ object.
            previous_token: Previous pagination reference.

        Returns:
            Reference value to retrieve next page.

        .. _requests.Response:
            https://requests.readthedocs.io/en/latest/api/#requests.Response
        """
        records = response.json()
        if not isinstance(records, list) or len(records) < self.page_size:
            return None
        return 2 if previous_token is None else int(previous_token) + 1

    @override
    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        return {"page": next_page_token or 1, "per_page": self.page_size}
