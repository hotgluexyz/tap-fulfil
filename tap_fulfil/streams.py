"""Stream type classes for tap-fulfil."""

from __future__ import annotations

from hotglue_singer_sdk import typing as th  # JSON Schema typing helpers

from tap_fulfil.client import FulfilStream


class AccountsStream(FulfilStream):
    """Fulfil chart-of-accounts records."""

    name = "accounts"
    path = "/model/account"
    primary_keys = ("id",)
    request_fields = ("id", "code", "name", "rec_name", "company")
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("code", th.StringType),
        th.Property("name", th.StringType),
        th.Property("rec_name", th.StringType),
        th.Property("company", th.IntegerType),
    ).to_dict()


class ContactsStream(FulfilStream):
    """Fulfil contacts, including supplier contacts."""

    name = "contacts"
    path = "/model/contact"
    primary_keys = ("id",)
    request_fields = (
        "id",
        "name",
        "full_name",
        "email",
        "active",
        "is_supplier",
        "addresses",
    )
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("full_name", th.StringType),
        th.Property("email", th.StringType),
        th.Property("active", th.BooleanType),
        th.Property("is_supplier", th.BooleanType),
        th.Property("addresses", th.ArrayType(th.IntegerType)),
    ).to_dict()


class CurrenciesStream(FulfilStream):
    """Fulfil currencies used to translate invoice currency relationships."""

    name = "currencies"
    path = "/model/currency"
    primary_keys = ("id",)
    request_fields = ("id", "code", "name")
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("code", th.StringType),
        th.Property("name", th.StringType),
    ).to_dict()


class InvoicesStream(FulfilStream):
    """Fulfil invoices; the ETL selects approved supplier invoices."""

    name = "invoices"
    path = "/model/invoice"
    primary_keys = ("id",)
    request_filter = (("type", "=", "in"), ("state", "in", ("posted", "approved")))
    request_fields = (
        "id",
        "number",
        "rec_name",
        "type",
        "state",
        "company",
        "party",
        "currency",
        "invoice_date",
        "lines",
        "total_amount",
    )
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("number", th.StringType),
        th.Property("rec_name", th.StringType),
        th.Property("type", th.StringType),
        th.Property("state", th.StringType),
        th.Property("company", th.IntegerType),
        th.Property("party", th.IntegerType),
        th.Property("currency", th.IntegerType),
        th.Property("invoice_date", th.DateType),
        th.Property("lines", th.ArrayType(th.IntegerType)),
        th.Property("total_amount", th.NumberType),
    ).to_dict()


class InvoiceLinesStream(FulfilStream):
    """Fulfil line items for the supplier invoices exported to Airwallex."""

    name = "invoice_lines"
    path = "/model/invoice_line"
    primary_keys = ("id",)
    request_filter = (
        ("invoice.type", "=", "in"),
        ("invoice.state", "in", ("posted", "approved")),
    )
    request_fields = (
        "id",
        "invoice",
        "type",
        "account",
        "quantity",
        "unit_price",
        "description",
        "amount",
    )
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("invoice", th.IntegerType),
        th.Property("type", th.StringType),
        th.Property("account", th.IntegerType),
        th.Property("quantity", th.NumberType),
        th.Property("unit_price", th.NumberType),
        th.Property("description", th.StringType),
        th.Property("amount", th.NumberType),
    ).to_dict()
