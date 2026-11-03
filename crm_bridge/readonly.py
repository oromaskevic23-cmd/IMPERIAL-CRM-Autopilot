"""CRM-SOFFT read-only Supabase/PostgreSQL aggregate adapter.

The caller injects an externally authenticated, *least-privilege* database
connection. Nothing here accepts arbitrary SQL, credentials, raw leads,
customer details, or writable actions. No 24/7 connection is claimed.

Copyright (c) 2026 Alexander Nikolaevich Romaskevich (RomaskevicH).
"""
from __future__ import annotations

from datetime import datetime, timezone
import re

LABEL = re.compile(r"[A-Z][A-Z0-9_]{1,79}\Z")
MAX_ROWS = 2_000_000

# All statements have fixed literals and return aggregated counts ONLY.
QUERIES = {
    "lead_states": ("SELECT state, count(*)::bigint FROM "
                    "crm_sofft.lead_registry GROUP BY state ORDER BY state"),
    "task_states": ("SELECT state, count(*)::bigint FROM "
                    "crm_sofft.task_registry GROUP BY state ORDER BY state"),
    "registered_workspaces": "SELECT count(*)::bigint FROM crm_sofft.workspace_registry",
    "registered_agent_records": "SELECT count(*)::bigint FROM crm_sofft.agent_registry",
    "payment_records": "SELECT count(*)::bigint FROM crm_sofft.payment_records",
    "revenue_ledger_entries": "SELECT count(*)::bigint FROM crm_sofft.revenue_ledger",
}
AUTHORITY = ("SELECT current_setting('transaction_read_only'), "
             "coalesce((SELECT rolsuper OR rolbypassrls "
             "FROM pg_catalog.pg_roles WHERE rolname=current_user), TRUE)")


class BridgeDenied(PermissionError):
    """Reject unsafe credential, query or database boundaries."""


def _count(value):
    if type(value) is not int or not 0 <= value <= MAX_ROWS:
        raise BridgeDenied("INVALID_AGGREGATE_COUNT")
    return value


def _group_rows(rows):
    if type(rows) not in (list, tuple) or len(rows) > 90:
        raise BridgeDenied("INVALID_GROUP_RESULT")
    result = {}
    for row in rows:
        if (type(row) not in (list, tuple) or len(row) != 2
                or type(row[0]) is not str or LABEL.fullmatch(row[0]) is None
                or row[0] in result):
            raise BridgeDenied("INVALID_STATE_LABEL")
        result[row[0]] = _count(row[1])
    return result


def inspect_counts(connection, *, observed_at: datetime | None = None):
    """One bounded read-only PostgreSQL transaction, with zero raw records.

    Requires an external psycopg-compatible connection (including .transaction
    and .execute); refuses superuser/BYPASSRLS. The caller MUST already
    constrain network, DB role, schema grants and trust before calling.
    """
    if connection is None or not callable(getattr(connection, "transaction", None)):
        raise BridgeDenied("MISSING_EXTERNAL_DATABASE_CONNECTION")
    observed_at = observed_at or datetime.now(timezone.utc)
    if observed_at.tzinfo is None or observed_at.utcoffset() is None:
        raise BridgeDenied("OBSERVATION_REQUIRES_TIMEZONE")
    with connection.transaction():
        connection.execute("SET TRANSACTION READ ONLY")
        connection.execute("SET LOCAL statement_timeout = '3000ms'")
        current = connection.execute(AUTHORITY).fetchone()
        if (type(current) not in (list, tuple) or len(current) != 2
                or current[0] != "on" or current[1] is not False):
            raise BridgeDenied("PRIVILEGED_OR_WRITABLE_DATABASE_ROLE_DENIED")
        lead_states = _group_rows(connection.execute(QUERIES["lead_states"]).fetchall())
        task_states = _group_rows(connection.execute(QUERIES["task_states"]).fetchall())
        totals = {}
        for name in (
            "registered_workspaces", "registered_agent_records",
            "payment_records", "revenue_ledger_entries"
        ):
            row = connection.execute(QUERIES[name]).fetchone()
            if type(row) not in (list, tuple) or len(row) != 1:
                raise BridgeDenied("INVALID_SINGLE_AGGREGATE")
            totals[name] = _count(row[0])
    return {
        "schema_version": 1,
        "source": "EXTERNAL_PRIVATE_READONLY_DB_AGGREGATE",
        "observed_at": observed_at.astimezone(timezone.utc).isoformat(),
        "lead_states": lead_states,
        "task_states": task_states,
        "totals": totals,
        "raw_customer_records_returned": 0,
        "database_write_performed": False,
        "read_role_must_be_provisioned_externally": True,
        "public_dashboard_authorized": False,
        "revenue_confirmed_by_provider": False,
        "production_nca_dispatch_authorized": False,
    }
