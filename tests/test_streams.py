"""Tests for Fulfil REST request construction."""

from tap_fulfil.streams import (
    AccountsStream,
    ContactsStream,
    CurrenciesStream,
    InvoiceLinesStream,
    InvoicesStream,
)
from tap_fulfil.tap import TapFulfil


def test_streams_request_their_declared_fields():
    """Each endpoint requests the fields required by its mapping schema."""
    tap = TapFulfil(config={"access_key": "placeholder"})

    for stream_type in (
        AccountsStream,
        ContactsStream,
        CurrenciesStream,
        InvoicesStream,
        InvoiceLinesStream,
    ):
        stream = stream_type(tap=tap)
        params = stream.get_url_params(context=None, next_page_token=None)

        assert params["page"] == 1
        assert params["per_page"] == 100
        assert params["fields"] == ",".join(stream.request_fields)
        assert stream.replication_key is None
        if stream.request_filter:
            assert "filter" in params
