"""Adversarial release-gate tests — only synthetic non-PII aggregates."""
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import unittest

from crm_control.release_gate import BLOCKED_ACTIONS, GATES, GateDenied, evaluate


OBSERVED = datetime(2026, 11, 3, 12, 0, tzinfo=timezone.utc)


def fixture():
    return {
        "schema_version": 1,
        "source_class": "READ_ONLY_CONNECTED_PROJECT_AGGREGATES",
        "observed_at": OBSERVED.isoformat(),
        "workspace_status": {"CONFIGURING": 2},
        "agent_production_state": {"REGISTERED_NOT_AUTHORIZED": 3},
        "agent_guardian_state": {"NOT_VERIFIED": 3},
        "lead_state": {"NEEDS_QUALIFICATION": 1,
                       "RESEARCH_ONLY_NOT_A_VERIFIED_BUYER": 2,
                       "OUTREACH_SENT_WAITING_REPLY": 1},
        "task_state": {"DRAFT": 4, "BLOCKED": 1},
        "payment_rows": 0,
        "revenue_rows": 0,
        "verified_gates": {name: False for name in GATES},
    }


class CRMReleaseGateTests(unittest.TestCase):
    def run_gate(self, obj=None, **kw):
        return evaluate(fixture() if obj is None else obj, now=kw.get("now", OBSERVED))

    def test_01_snapshot_produces_blocked_release(self):
        output = self.run_gate()
        self.assertEqual(output["release_state"], "PRODUCTION_EXECUTION_BLOCKED")
        self.assertFalse(output["production_authorized"])
        self.assertFalse(output["hanter_production_connection_verified"])
        self.assertFalse(output["independent_attestation_verified"])

    def test_02_five_sensitive_actions_are_explicitly_denied(self):
        self.assertEqual(
            self.run_gate()["sensitive_actions"],
            {name: "DENY" for name in BLOCKED_ACTIONS}
        )

    def test_03_summary_contains_only_aggregates(self):
        output = self.run_gate()
        self.assertEqual(output["workspace_records"], 2)
        self.assertEqual(output["registered_nca_records"], 3)
        self.assertEqual(output["leads_needing_qualification"], 1)
        self.assertEqual(output["research_only_leads"], 2)
        self.assertEqual(output["draft_tasks"], 4)
        self.assertEqual(output["blocked_tasks"], 1)
        self.assertIsNone(output["professional_nca_active_count"])
        self.assertFalse(output["public_publishable"])

    def test_04_owner_passport_and_guardian_gaps_are_reported(self):
        reasons = self.run_gate()["reason_codes"]
        for required in ("MISSING_SIGNED_AI_PASSPORT_VERIFIED",
                         "MISSING_OWNER_IDENTITY_ENROLLED",
                         "MISSING_GUARDIAN_CORE_VERIFIED",
                         "REGISTERED_AGENTS_LACK_PRODUCTION_AUTHORITY"):
            self.assertIn(required, reasons)

    def test_05_unrecognized_source_is_rejected(self):
        data = fixture()
        data["source_class"] = "PRODUCTION_SIGNED_AND_AUTHORITATIVE"
        with self.assertRaisesRegex(GateDenied, "UNSUPPORTED_SOURCE_CLASS"):
            self.run_gate(data)

    def test_06_forbidden_customer_identifier_field_is_rejected(self):
        data = fixture()
        data["customer_email"] = "hidden@example.invalid"
        with self.assertRaisesRegex(GateDenied, "UNEXPECTED_SNAPSHOT_SCHEMA"):
            self.run_gate(data)

    def test_07_missing_field_is_rejected(self):
        data = fixture()
        del data["agent_guardian_state"]
        with self.assertRaises(GateDenied):
            self.run_gate(data)

    def test_08_bad_version_is_rejected(self):
        data = fixture()
        data["schema_version"] = True
        with self.assertRaisesRegex(GateDenied, "UNEXPECTED_VERSION"):
            self.run_gate(data)

    def test_09_negative_record_count_is_rejected(self):
        data = fixture()
        data["task_state"]["DRAFT"] = -1
        with self.assertRaisesRegex(GateDenied, "INVALID_AGGREGATE_COUNT"):
            self.run_gate(data)

    def test_10_boolean_is_not_a_count(self):
        data = fixture()
        data["payment_rows"] = True
        with self.assertRaisesRegex(GateDenied, "INVALID_AGGREGATE_COUNT"):
            self.run_gate(data)

    def test_11_large_count_is_denied(self):
        data = fixture()
        data["agent_production_state"]["REGISTERED_NOT_AUTHORIZED"] = 999999999
        with self.assertRaises(GateDenied):
            self.run_gate(data)

    def test_12_script_injection_state_is_denied(self):
        data = fixture()
        data["lead_state"] = {"<script>alert(1)</script>": 1}
        with self.assertRaisesRegex(GateDenied, "BAD_STATE_LEAD"):
            self.run_gate(data)

    def test_13_agent_production_and_guardian_totals_must_agree(self):
        data = fixture()
        data["agent_guardian_state"]["NOT_VERIFIED"] = 2
        with self.assertRaisesRegex(GateDenied, "AGENT_POPULATION_MISMATCH"):
            self.run_gate(data)

    def test_14_missing_approval_flag_denied(self):
        data = fixture()
        del data["verified_gates"]["approval_gateway_verified"]
        with self.assertRaisesRegex(GateDenied, "INVALID_PROOF_FLAGS"):
            self.run_gate(data)

    def test_15_forged_string_boolean_is_denied(self):
        data = fixture()
        data["verified_gates"]["owner_identity_enrolled"] = "true"
        with self.assertRaisesRegex(GateDenied, "INVALID_PROOF_FLAGS"):
            self.run_gate(data)

    def test_16_stale_snapshot_cannot_authorize_review(self):
        with self.assertRaisesRegex(GateDenied, "SNAPSHOT_STALE_OR_FUTURE"):
            self.run_gate(now=OBSERVED + timedelta(hours=2))

    def test_17_future_timestamp_fails_closed(self):
        with self.assertRaisesRegex(GateDenied, "SNAPSHOT_STALE_OR_FUTURE"):
            self.run_gate(now=OBSERVED - timedelta(minutes=2))

    def test_18_time_zone_is_required(self):
        data = fixture()
        data["observed_at"] = "2026-11-03T12:00:00"
        with self.assertRaisesRegex(GateDenied, "NAIVE_SNAPSHOT_TIME"):
            self.run_gate(data)

    def test_19_self_asserted_all_true_flags_do_not_grant_authority(self):
        data = fixture()
        data["verified_gates"] = {name: True for name in GATES}
        data["workspace_status"] = {"ACTIVE": 1}
        data["agent_production_state"] = {"APPROVED": 2}
        data["agent_guardian_state"] = {"VERIFIED": 2}
        data["lead_state"] = {}
        data["task_state"] = {}
        output = self.run_gate(data)
        self.assertEqual(output["reason_codes"], [])
        self.assertFalse(output["production_authorized"])
        self.assertFalse(output["independent_attestation_verified"])
        self.assertTrue(all(v == "DENY" for v in output["sensitive_actions"].values()))

    def test_20_positive_payment_rows_are_not_confirmed_revenue(self):
        data = fixture()
        data["payment_rows"] = 2
        data["revenue_rows"] = 3
        out = self.run_gate(data)
        self.assertEqual(out["recorded_payment_rows"], 2)
        self.assertIsNone(out["provider_confirmed_revenue"])
        self.assertEqual(out["sensitive_actions"]["PAYMENT_CONFIRMED"], "DENY")

    def test_21_normalization_is_deterministic_for_identical_timestamp(self):
        self.assertEqual(self.run_gate()["input_integrity_digest_sha256"],
                         self.run_gate()["input_integrity_digest_sha256"])

    def test_22_digest_changes_with_source_count(self):
        data = fixture()
        data["lead_state"]["NEEDS_QUALIFICATION"] = 3
        self.assertNotEqual(self.run_gate()["input_integrity_digest_sha256"],
                            self.run_gate(data)["input_integrity_digest_sha256"])

    def test_23_unknown_states_are_not_auto_approved(self):
        data = fixture()
        data["task_state"] = {"UNREVIEWED_UNKNOWN": 5}
        out = self.run_gate(data)
        self.assertFalse(out["production_authorized"])

    def test_24_no_client_contact_even_when_leads_wait(self):
        out = self.run_gate()
        self.assertEqual(out["leads_awaiting_reply"], 1)
        self.assertEqual(out["sensitive_actions"]["CUSTOMER_OUTREACH"], "DENY")
        self.assertEqual(out["external_effects"], 0)

    def test_25_federated_architecture_without_real_dispatch(self):
        out = self.run_gate()
        self.assertTrue(out["federated_orchestrators_supported"])
        self.assertFalse(out["hanter_production_connection_verified"])

    def test_26_root_role_change_unconditionally_denied(self):
        out = self.run_gate()
        self.assertEqual(out["sensitive_actions"]["ROOT_ROLE_CHANGE"], "DENY")


if __name__ == "__main__":
    unittest.main()
