"""One-shot synthetic readiness test, never a production authority service."""
from __future__ import annotations
import json
from datetime import datetime, timezone
from .release_gate import GATES, evaluate


def main():
    instant = datetime.now(timezone.utc)
    demo = {
        "schema_version": 1,
        "source_class": "READ_ONLY_CONNECTED_PROJECT_AGGREGATES",
        "observed_at": instant.isoformat(),
        "workspace_status": {"CONFIGURING": 2},
        "agent_production_state": {"REGISTERED_NOT_AUTHORIZED": 3},
        "agent_guardian_state": {"NOT_VERIFIED": 3},
        "lead_state": {"NEEDS_QUALIFICATION": 1, "RESEARCH_ONLY_NOT_A_VERIFIED_BUYER": 1},
        "task_state": {"DRAFT": 2, "BLOCKED": 1},
        "payment_rows": 0,
        "revenue_rows": 0,
        "verified_gates": {gate: False for gate in GATES}
    }
    result = evaluate(demo, now=instant)
    result["example_only"] = True
    result["synthetic_fixture_not_real_crm"] = True
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["production_authorized"] or any(x != "DENY" for x in result["sensitive_actions"].values()):
        raise SystemExit("FAIL_CLOSED_INVARIANT_BROKEN")


if __name__ == "__main__":
    main()
