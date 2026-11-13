"""Tests for Fulfil REST request construction."""

from urllib.parse import urlsplit

import pytest

from tap_fulfil.client import normalize_fulfil_value
from tap_fulfil.streams import (
    AccountsStream,
    ContactsStream,
    CurrenciesStream,
    InvoiceLinesStream,
    InvoicesStream,
)
from tap_fulfil.tap import TapFulfil


@pytest.mark.parametrize("config_key", ["base_url", "api_url"])
@pytest.mark.parametrize("suffix", ["", "/", "///", "/api/v2", "/api/v2/", "/api/v2///"])
@pytest.mark.parametrize(
    "stream_type",
    [AccountsStream, ContactsStream, CurrenciesStream, InvoicesStream, InvoiceLinesStream],
)
def test_workspace_and_legacy_urls_build_api_requests(config_key, suffix, stream_type):
    """Both config aliases produce exactly one API prefix for every endpoint."""
    tap = TapFulfil(
        config={"access_key": "placeholder", config_key: f"https://workspace.fulfil.io{suffix}"}
    )
    stream = stream_type(tap=tap)

    request = stream.prepare_request(context=None, next_page_token=None)

    assert request.url is not None
    assert urlsplit(request.url)._replace(query="").geturl() == (
        f"https://workspace.fulfil.io/api/v2{stream.path}"
    )


@pytest.mark.parametrize("base_suffix", ["", "/", "/api/v2", "/api/v2/"])
@pytest.mark.parametrize("api_suffix", ["", "/", "/api/v2", "/api/v2/"])
def test_base_url_takes_precedence_in_built_requests(base_suffix, api_suffix):
    """An explicit base_url wins over an explicit api_url in either URL form."""
    tap = TapFulfil(
        config={
            "access_key": "placeholder",
            "base_url": f"https://workspace.fulfil.io{base_suffix}",
            "api_url": f"https://other.fulfil.io{api_suffix}",
        }
    )
    request = AccountsStream(tap=tap).prepare_request(context=None, next_page_token=None)

    assert request.url is not None
    assert urlsplit(request.url)._replace(query="").geturl() == (
        "https://workspace.fulfil.io/api/v2/model/account"
    )


def test_default_workspace_url_builds_api_request():
    """The default workspace URL still targets the development API root."""
    tap = TapFulfil(config={"access_key": "placeholder"})
    request = AccountsStream(tap=tap).prepare_request(context=None, next_page_token=None)

    assert request.url is not None
    assert urlsplit(request.url)._replace(query="").geturl() == (
        "https://dev.fulfil.io/api/v2/model/account"
    )


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


def test_relationship_schemas_match_fulfil_id_payloads():
    """Fulfil returns relationship values as integer IDs, not nested objects."""
    tap = TapFulfil(config={"access_key": "placeholder"})

    accounts = AccountsStream(tap=tap).schema["properties"]
    contacts = ContactsStream(tap=tap).schema["properties"]
    invoices = InvoicesStream(tap=tap).schema["properties"]
    invoice_lines = InvoiceLinesStream(tap=tap).schema["properties"]

    assert accounts["company"]["type"] == ["integer", "null"]
    assert contacts["addresses"]["items"]["type"] == ["integer"]
    for field in ("company", "party", "currency"):
        assert invoices[field]["type"] == ["integer", "null"]
    assert invoices["lines"]["items"]["type"] == ["integer"]
    assert invoice_lines["invoice"]["type"] == ["integer", "null"]
    assert invoice_lines["account"]["type"] == ["integer", "null"]
