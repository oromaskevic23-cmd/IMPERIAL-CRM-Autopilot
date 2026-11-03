"""IMPERIAL Core / CRM-SOFFT: conservative operational release gate.

This gate consumes *aggregated, non-identifying* database posture snapshots.
It creates a review recommendation only. It NEVER issues an AI Passport,
contacts clients, grants permissions, changes Supabase, deploys workers or
confirms revenue. The input is NOT a trusted digital attestation.

Copyright (c) 2026 Alexander Nikolaevich Romaskevich (RomaskevicH).
"""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
import re

KEY = re.compile(r"[A-Z][A-Z0-9_]{1,79}\Z")
MAX_COUNT = 5_000_000
FIELDS = frozenset({
    "schema_version", "source_class", "observed_at", "workspace_status",
    "agent_production_state", "agent_guardian_state", "lead_state",
    "task_state", "payment_rows", "revenue_rows", "verified_gates"
})
GATES = frozenset({
    "owner_identity_enrolled", "signed_ai_passport_verified",
    "guardian_core_verified", "approval_gateway_verified",
    "independent_professional_qa", "managed_worker_heartbeat_verified",
    "owner_kill_switch_remotely_verified", "tenant_rls_verified",
    "client_mandate_verified", "provider_settlement_reconciled",
    "audit_ledger_signed"
})
BLOCKED_ACTIONS = (
    "NCA_PRODUCTION_DISPATCH", "CUSTOMER_OUTREACH", "PAYMENT_CONFIRMED",
    "PUBLIC_CUSTOMER_DATA_EXPORT", "ROOT_ROLE_CHANGE"
)


class GateDenied(ValueError):
    """The read-only release evaluation rejected an invalid input."""


def _count(value: object) -> int:
    if type(value) is not int or not 0 <= value <= MAX_COUNT:
        raise GateDenied("INVALID_AGGREGATE_COUNT")
    return value


def _group(value: object, key: str) -> dict:
    if type(value) is not dict or len(value) > 100:
        raise GateDenied("BAD_GROUP_" + key)
    checked = {}
    for state, count in value.items():
        if type(state) is not str or not KEY.fullmatch(state):
            raise GateDenied("BAD_STATE_" + key)
        checked[state] = _count(count)
    return checked


def _timestamp(value: object) -> datetime:
    if type(value) is not str or len(value) > 40:
        raise GateDenied("INVALID_SNAPSHOT_TIME")
    try:
        observed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise GateDenied("INVALID_SNAPSHOT_TIME") from None
    if observed.tzinfo is None or observed.utcoffset() is None:
        raise GateDenied("NAIVE_SNAPSHOT_TIME")
    return observed.astimezone(timezone.utc)


def evaluate(snapshot: object, *, now: datetime | None = None) -> dict:
    """Return only evidence gaps and HUMAN REVIEW instructions; no authority."""
    if type(snapshot) is not dict or set(snapshot) != FIELDS:
        raise GateDenied("UNEXPECTED_SNAPSHOT_SCHEMA")
    if snapshot["schema_version"] != 1 or type(snapshot["schema_version"]) is not int:
        raise GateDenied("UNEXPECTED_VERSION")
    if snapshot["source_class"] != "READ_ONLY_CONNECTED_PROJECT_AGGREGATES":
        raise GateDenied("UNSUPPORTED_SOURCE_CLASS")
    stamp = _timestamp(snapshot["observed_at"])
    now = now or datetime.now(timezone.utc)
    if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() is None:
        raise GateDenied("INVALID_VERIFICATION_CLOCK")
    age = (now.astimezone(timezone.utc) - stamp).total_seconds()
    if not -60 <= age <= 30 * 60:
        raise GateDenied("SNAPSHOT_STALE_OR_FUTURE")

    groups = {
        "workspace_status": _group(snapshot["workspace_status"], "WORKSPACE"),
        "agent_production_state": _group(snapshot["agent_production_state"], "AGENT"),
        "agent_guardian_state": _group(snapshot["agent_guardian_state"], "GUARDIAN"),
        "lead_state": _group(snapshot["lead_state"], "LEAD"),
        "task_state": _group(snapshot["task_state"], "TASK")
    }
    agent_total = sum(groups["agent_production_state"].values())
    if agent_total != sum(groups["agent_guardian_state"].values()):
        raise GateDenied("AGENT_POPULATION_MISMATCH")
    payments = _count(snapshot["payment_rows"])
    ledger = _count(snapshot["revenue_rows"])
    gates = snapshot["verified_gates"]
    if type(gates) is not dict or set(gates) != GATES or any(type(v) is not bool for v in gates.values()):
        raise GateDenied("INVALID_PROOF_FLAGS")

    reasons = []
    if groups["workspace_status"].get("CONFIGURING", 0):
        reasons.append("WORKSPACES_NOT_READY")
    if groups["agent_production_state"].get("REGISTERED_NOT_AUTHORIZED", 0):
        reasons.append("REGISTERED_AGENTS_LACK_PRODUCTION_AUTHORITY")
    if groups["agent_guardian_state"].get("NOT_VERIFIED", 0):
        reasons.append("AGENTS_GUARDIAN_NOT_VERIFIED")
    if groups["task_state"].get("BLOCKED", 0):
        reasons.append("BLOCKED_TASKS_REQUIRE_REVIEW")
    if groups["lead_state"].get("RESEARCH_ONLY_NOT_A_VERIFIED_BUYER", 0):
        reasons.append("RESEARCH_LEADS_NOT_BUYERS")
    if groups["lead_state"].get("NEEDS_QUALIFICATION", 0):
        reasons.append("LEADS_REQUIRE_VERIFIED_MANDATE")
    for name in sorted(GATES):
        if not gates[name]:
            reasons.append("MISSING_" + name.upper())

    # Even a self-asserted all-true flag set cannot confer authority.
    # No protected issuer or independent attestation is connected here.
    reason_set = tuple(dict.fromkeys(reasons))
    normalized = {
        "schema_version": 1, "observed_at": stamp.isoformat(),
        "groups": groups, "payment_rows": payments, "revenue_rows": ledger,
        "verified_gates": gates
    }
    digest = sha256(json.dumps(
        normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")).hexdigest()
    return {
        "schema_version": 1,
        "product": "IMPERIAL Core / CRM-SOFFT",
        "source_claim": "CALLER_SUPPLIED_UNATTESTED_AGGREGATES",
        "observed_at": stamp.isoformat(),
        "source_age_seconds": int(age),
        "input_integrity_digest_sha256": digest,
        "workspace_records": sum(groups["workspace_status"].values()),
        "registered_nca_records": agent_total,
        "leads_needing_qualification": groups["lead_state"].get("NEEDS_QUALIFICATION", 0),
        "research_only_leads": groups["lead_state"].get("RESEARCH_ONLY_NOT_A_VERIFIED_BUYER", 0),
        "leads_awaiting_reply": groups["lead_state"].get("OUTREACH_SENT_WAITING_REPLY", 0),
        "draft_tasks": groups["task_state"].get("DRAFT", 0),
        "blocked_tasks": groups["task_state"].get("BLOCKED", 0),
        "recorded_payment_rows": payments,
        "recorded_revenue_ledger_rows": ledger,
        "provider_confirmed_revenue": None,
        "professional_nca_active_count": None,
        "release_state": "PRODUCTION_EXECUTION_BLOCKED",
        "sensitive_actions": {action: "DENY" for action in BLOCKED_ACTIONS},
        "reason_codes": list(reason_set),
        "first_safe_action": "HUMAN_REVIEW_ONE_LEAD_AND_VERIFY_AI_PASSPORT",
        "federated_orchestrators_supported": True,
        "hanter_production_connection_verified": False,
        "independent_attestation_verified": False,
        "production_authorized": False,
        "public_publishable": False,
        "external_effects": 0
    }
