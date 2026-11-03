"""CRM-SOFFT fact-only HANTER triage planner.

Inputs must be aggregate counts from a private, read-only server query.
Outputs are REVIEW PROPOSALS. No customer details, agent deployment,
outreach, purchases, or payment confirmations are issued.
"""
from __future__ import annotations
from datetime import datetime, timezone
import re

from .readonly import BridgeDenied, _count

STATE = re.compile(r"[A-Z][A-Z0-9_]{1,79}\Z")
NEXT_STEP = {
    "NEEDS_QUALIFICATION": ("VERIFY_CLIENT_MANDATE", "HUMAN_QUALIFICATION_REQUIRED"),
    "OUTREACH_SENT_WAITING_REPLY": ("WAIT_FOR_REPLY", "NO_DUPLICATE_OUTREACH"),
    "RESEARCH_ONLY_NOT_A_VERIFIED_BUYER": ("RESEARCH_ONLY", "NOT_A_CONFIRMED_BUYER"),
    "QUALIFIED": ("REVIEW_SCOPE_AND_CONSENT", "APPROVAL_GATEWAY_REQUIRED"),
    "DEMAND_FOUND": ("VERIFY_SOURCE_AND_PLATFORM_RIGHTS", "NO_CONTACT_WITHOUT_APPROVAL"),
    "DRAFT": ("REVIEW_TASK_SCOPE_AND_PASSPORT", "DO_NOT_DISPATCH"),
    "BLOCKED": ("INVESTIGATE_BLOCKER", "DO_NOT_DISPATCH"),
}
VERTICALS = {
    "AI_SERVICES": "AI Services Domain Orchestrator",
    "FREELANCE": "Freelance Domain Orchestrator",
    "AUTOMATION": "Automation Domain Orchestrator",
    "REAL_ESTATE": "Real Estate Domain Orchestrator",
    "BROKERAGE": "Brokerage Domain Orchestrator",
    "DIGITAL_PRODUCTS": "Digital Products Domain Orchestrator"
}
NCA_ROLES = ("Opportunity Scout", "Solution Architect",
             "Implementation Specialist", "Independent QA", "Delivery Reviewer")


def _utc_time(value):
    if type(value) is not str:
        raise BridgeDenied("INVALID_OBSERVATION_TIME")
    try:
        stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise BridgeDenied("INVALID_OBSERVATION_TIME") from None
    if stamp.tzinfo is None or stamp.utcoffset() is None:
        raise BridgeDenied("INVALID_OBSERVATION_TIME")
    return stamp.astimezone(timezone.utc)


def _states(rows):
    if type(rows) is not dict or len(rows) > 90:
        raise BridgeDenied("INVALID_GROUPED_STATES")
    for key, value in rows.items():
        if type(key) is not str or not STATE.fullmatch(key):
            raise BridgeDenied("INVALID_AGGREGATE_LABEL")
        _count(value)
    return rows


def draft_hanter_review(snapshot, *, now=None, domain="AI_SERVICES"):
    if (type(snapshot) is not dict or
            set(snapshot) != {"schema_version","source","observed_at","lead_states",
                              "task_states","totals","raw_customer_records_returned",
                              "database_write_performed","read_role_must_be_provisioned_externally",
                              "public_dashboard_authorized","revenue_confirmed_by_provider",
                              "production_nca_dispatch_authorized"} or
            snapshot["schema_version"] != 1 or
            snapshot["source"] != "EXTERNAL_PRIVATE_READONLY_DB_AGGREGATE"):
        raise BridgeDenied("UNKNOWN_PRIVATE_SNAPSHOT")
    if (snapshot["raw_customer_records_returned"] != 0 or
            snapshot["database_write_performed"] is not False or
            snapshot["public_dashboard_authorized"] is not False or
            snapshot["production_nca_dispatch_authorized"] is not False or
            snapshot["revenue_confirmed_by_provider"] is not False):
        raise BridgeDenied("UNSAFE_REPORTED_SOURCE_SCOPE")
    if domain not in VERTICALS:
        raise BridgeDenied("UNKNOWN_FEDERATED_DOMAIN")
    stamp = _utc_time(snapshot["observed_at"])
    now = now or datetime.now(timezone.utc)
    if not isinstance(now,datetime) or now.tzinfo is None or now.utcoffset() is None:
        raise BridgeDenied("INVALID_CLOCK")
    diff = (now.astimezone(timezone.utc)-stamp).total_seconds()
    if not -30 <= diff <= 30*60:
        raise BridgeDenied("STALE_OR_FUTURE_AGGREGATE")
    lead_states, task_states = _states(snapshot["lead_states"]), _states(snapshot["task_states"])
    totals = snapshot["totals"]
    if (type(totals) is not dict or
            set(totals)!={"registered_workspaces","registered_agent_records",
                          "payment_records","revenue_ledger_entries"}):
        raise BridgeDenied("INVALID_TOTALS_SCHEMA")
    for val in totals.values():
        _count(val)
    review = []
    for label, count in lead_states.items():
        if count == 0:
            continue
        action, guard = NEXT_STEP.get(label,("MANUAL_POLICY_CLASSIFICATION","UNKNOWN_LEAD_STATE"))
        review.append({"kind":"LEAD_TRIAGE","source_state":label,"count":count,
                       "proposed_action":action,"gate":guard})
    for label, count in task_states.items():
        if count == 0:
            continue
        action, guard = NEXT_STEP.get(label,("MANUAL_TASK_CLASSIFICATION","UNKNOWN_TASK_STATE"))
        review.append({"kind":"TASK_TRIAGE","source_state":label,"count":count,
                       "proposed_action":action,"gate":guard})
    if totals["payment_records"] or totals["revenue_ledger_entries"]:
        review.append({"kind":"PAYMENT_RECONCILIATION",
                       "source_state":"UNRECONCILED_AGGREGATE_COUNTS",
                       "count":totals["payment_records"],
                       "proposed_action":"INDEPENDENT_PROVIDER_RECONCILIATION",
                       "gate":"NO_PAYMENT_CONFIRMED_FROM_ROW_COUNT"})
    return {
        "schema_version":1,"route_type":"HANTER_REVIEW_PROPOSAL_ONLY",
        "observed_at":stamp.isoformat(),
        "source_age_seconds":int(diff),
        "hanteR_command_center":"HANTER",
        "domain_orchestrator":VERTICALS[domain],
        "planned_nca_roles":list(NCA_ROLES),
        "case_specific_routing":False,
        "actual_nca_workers_started":0,
        "owner_approval_verified":False,
        "ai_passport_verified":False,
        "guardian_core_approved":False,
        "approval_gateway_approved":False,
        "client_contact_authorized":False,
        "server_dispatch_authorized":False,
        "confirmed_payments":None,
        "confirmed_revenue_minor":None,
        "next_steps":review,
        "read_only":True,
        "public_publishable":False,
        "personal_data_present":False
    }
