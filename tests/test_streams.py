"""Tests for Fulfil REST request construction."""

from tap_fulfil.client import normalize_fulfil_value
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


def test_normalize_fulfil_typed_values():
    """Fulfil's typed values conform to the Singer schema before emission."""
    record = {
        "total_amount": {"__class__": "Decimal", "decimal": "100.00"},
        "invoice_date": {"__class__": "date", "iso_string": "2026-10-25"},
        "lines": [{"unit_price": {"__class__": "Decimal", "decimal": "12.50"}}],
    }

    assert normalize_fulfil_value(record) == {
        "total_amount": 100.0,
        "invoice_date": "2026-10-25",
        "lines": [{"unit_price": 12.5}],
    }
