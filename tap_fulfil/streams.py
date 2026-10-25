"""Stream type classes for tap-fulfil."""

from __future__ import annotations

from hotglue_singer_sdk import typing as th  # JSON Schema typing helpers

from tap_fulfil.client import FulfilStream


class AccountsStream(FulfilStream):
    """Fulfil chart-of-accounts records."""

    name = "accounts"
    path = "/model/account"
    primary_keys = ("id",)
    replication_key = "updated_at"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("code", th.StringType),
        th.Property("name", th.StringType),
        th.Property("rec_name", th.StringType),
        th.Property("active", th.BooleanType),
        th.Property("company", th.CustomType({"type": ["object", "integer", "null"]})),
        th.Property("updated_at", th.DateTimeType),
    ).to_dict()


class ContactsStream(FulfilStream):
    """Fulfil contacts, including supplier contacts."""

    name = "contacts"
    path = "/model/contact"
    primary_keys = ("id",)
    replication_key = "updated_at"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("full_name", th.StringType),
        th.Property("email", th.StringType),
        th.Property("active", th.BooleanType),
        th.Property("is_supplier", th.BooleanType),
        th.Property("addresses", th.ArrayType(th.CustomType({"type": "object"}))),
        th.Property("updated_at", th.DateTimeType),
    ).to_dict()


class CurrenciesStream(FulfilStream):
    """Fulfil currencies used to translate invoice currency relationships."""

    name = "currencies"
    path = "/model/currency"
    primary_keys = ("id",)
    replication_key = "updated_at"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("code", th.StringType),
        th.Property("name", th.StringType),
        th.Property("updated_at", th.DateTimeType),
    ).to_dict()


class InvoicesStream(FulfilStream):
    """Fulfil invoices; the ETL selects approved supplier invoices."""

    name = "invoices"
    path = "/model/invoice"
    primary_keys = ("id",)
    replication_key = "updated_at"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("number", th.StringType),
        th.Property("rec_name", th.StringType),
        th.Property("type", th.StringType),
        th.Property("state", th.StringType),
        th.Property("company", th.CustomType({"type": ["object", "integer", "null"]})),
        th.Property("party", th.CustomType({"type": ["object", "integer", "null"]})),
        th.Property("currency", th.CustomType({"type": ["object", "integer", "null"]})),
        th.Property("invoice_date", th.DateType),
        th.Property("payment_term_date", th.DateType),
        th.Property("lines", th.ArrayType(th.CustomType({"type": "object"}))),
        th.Property("total_amount", th.NumberType),
        th.Property("updated_at", th.DateTimeType),
    ).to_dict()
