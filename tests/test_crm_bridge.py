"""Adversarial tests for aggregate-only CRM-SOFFT bridge and HANTER review.

Synthetic fake SQL responses only. No real clients, workers or credentials.
"""
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import copy
import unittest

from crm_bridge import BridgeDenied, inspect_counts, draft_hanter_review
from crm_bridge.readonly import AUTHORITY, QUERIES


STAMP = datetime(2026,11,3,8,30,0,tzinfo=timezone.utc)


class Cursor:
    def __init__(self, *, one=None, many=None):
        self.one = one
        self.many = many
    def fetchone(self):
        return self.one
    def fetchall(self):
        return self.many


class FakeDB:
    def __init__(self, *, authority=("on",False), lead=None, task=None, totals=None):
        self.authority = authority
        self.lead = lead if lead is not None else [
            ("NEEDS_QUALIFICATION",2),
            ("RESEARCH_ONLY_NOT_A_VERIFIED_BUYER",3),
            ("OUTREACH_SENT_WAITING_REPLY",1)]
        self.task = task if task is not None else [("DRAFT",4),("BLOCKED",1)]
        self.totals = totals if totals is not None else {
            "registered_workspaces":3, "registered_agent_records":5,
            "payment_records":0, "revenue_ledger_entries":0}
        self.statements = []
        self.entered = False
        self.exited = False

    @contextmanager
    def transaction(self):
        self.entered = True
        try:
            yield
        finally:
            self.exited = True

    def execute(self,sql):
        self.statements.append(sql)
        if sql in ("SET TRANSACTION READ ONLY", "SET LOCAL statement_timeout = '3000ms'"):
            return Cursor()
        if sql == AUTHORITY:
            return Cursor(one=self.authority)
        if sql == QUERIES["lead_states"]:
            return Cursor(many=self.lead)
        if sql == QUERIES["task_states"]:
            return Cursor(many=self.task)
        for key in self.totals:
            if sql == QUERIES[key]:
                return Cursor(one=(self.totals[key],))
        raise AssertionError("Unexpected SQL statement")


class BridgeTests(unittest.TestCase):
    def snapshot(self,db=None):
        return inspect_counts(db or FakeDB(),observed_at=STAMP)

    def plan(self,db=None,**kw):
        return draft_hanter_review(self.snapshot(db),now=STAMP,**kw)

    def test_01_exact_fixed_aggregate_sql(self):
        db=FakeDB()
        self.snapshot(db)
        self.assertEqual(db.statements[0],"SET TRANSACTION READ ONLY")
        self.assertEqual(db.statements[1],"SET LOCAL statement_timeout = '3000ms'")
        self.assertEqual(db.statements[2],AUTHORITY)
        self.assertEqual(set(db.statements[3:]),set(QUERIES.values()))
        self.assertTrue(db.entered and db.exited)

    def test_02_sql_has_no_raw_customer_data_fields(self):
        for query in QUERIES.values():
            self.assertTrue(query.upper().startswith("SELECT"))
            self.assertNotIn("SELECT *",query.upper())
            for prohibited in ("source_ref","source_receipt_hash","client_id",
                               "amount","provider","need","source_text","passkey"):
                self.assertNotIn(prohibited,query.lower())

    def test_03_snapshot_uses_aggregates_only(self):
        snap=self.snapshot()
        self.assertEqual(snap["totals"]["registered_workspaces"],3)
        self.assertEqual(snap["lead_states"]["NEEDS_QUALIFICATION"],2)
        self.assertEqual(snap["raw_customer_records_returned"],0)
        self.assertFalse(snap["production_nca_dispatch_authorized"])

    def test_04_no_connection_fails_closed(self):
        with self.assertRaisesRegex(BridgeDenied,"MISSING_EXTERNAL_DATABASE_CONNECTION"):
            inspect_counts(None,observed_at=STAMP)

    def test_05_superuser_bypassrls_denied(self):
        with self.assertRaisesRegex(BridgeDenied,"PRIVILEGED_OR_WRITABLE"):
            self.snapshot(FakeDB(authority=("on",True)))

    def test_06_read_write_role_denied(self):
        with self.assertRaisesRegex(BridgeDenied,"PRIVILEGED_OR_WRITABLE"):
            self.snapshot(FakeDB(authority=("off",False)))

    def test_07_unverified_authority_fails_closed(self):
        with self.assertRaisesRegex(BridgeDenied,"PRIVILEGED_OR_WRITABLE"):
            self.snapshot(FakeDB(authority=("on",None)))

    def test_08_negative_count_denied(self):
        with self.assertRaisesRegex(BridgeDenied,"INVALID_AGGREGATE_COUNT"):
            self.snapshot(FakeDB(lead=[("NEEDS_QUALIFICATION",-1)]))

    def test_09_boolean_count_denied(self):
        with self.assertRaisesRegex(BridgeDenied,"INVALID_AGGREGATE_COUNT"):
            self.snapshot(FakeDB(totals={
                "registered_workspaces":True,"registered_agent_records":1,
                "payment_records":0,"revenue_ledger_entries":0}))

    def test_10_injected_source_label_rejected(self):
        with self.assertRaisesRegex(BridgeDenied,"INVALID_STATE_LABEL"):
            self.snapshot(FakeDB(lead=[("<script>alert(1)</script>",1)]))

    def test_11_duplicated_status_rejected(self):
        with self.assertRaisesRegex(BridgeDenied,"INVALID_STATE_LABEL"):
            self.snapshot(FakeDB(lead=[("DRAFT",1),("DRAFT",2)]))

    def test_12_stale_observation_rejected(self):
        with self.assertRaisesRegex(BridgeDenied,"STALE_OR_FUTURE"):
            draft_hanter_review(self.snapshot(),now=STAMP+timedelta(hours=1))

    def test_13_future_observation_rejected(self):
        with self.assertRaisesRegex(BridgeDenied,"STALE_OR_FUTURE"):
            draft_hanter_review(self.snapshot(),now=STAMP-timedelta(minutes=10))

    def test_14_research_only_does_not_count_as_buyer(self):
        proposal=self.plan()
        entry=next(x for x in proposal["next_steps"]
                   if x["source_state"]=="RESEARCH_ONLY_NOT_A_VERIFIED_BUYER")
        self.assertEqual(entry["proposed_action"],"RESEARCH_ONLY")
        self.assertEqual(entry["gate"],"NOT_A_CONFIRMED_BUYER")
        self.assertFalse(proposal["client_contact_authorized"])

    def test_15_existing_outreach_never_auto_resends(self):
        proposal=self.plan()
        entry=next(x for x in proposal["next_steps"]
                   if x["source_state"]=="OUTREACH_SENT_WAITING_REPLY")
        self.assertEqual(entry["gate"],"NO_DUPLICATE_OUTREACH")

    def test_16_qualification_requires_human_review(self):
        entry=next(x for x in self.plan()["next_steps"]
                   if x["source_state"]=="NEEDS_QUALIFICATION")
        self.assertEqual(entry["gate"],"HUMAN_QUALIFICATION_REQUIRED")

    def test_17_blocked_tasks_stay_blocked(self):
        entry=next(x for x in self.plan()["next_steps"]
                   if x["source_state"]=="BLOCKED")
        self.assertEqual(entry["gate"],"DO_NOT_DISPATCH")

    def test_18_multi_orchestrator_domain_selection(self):
        realestate=self.plan(domain="REAL_ESTATE")
        automation=self.plan(domain="AUTOMATION")
        self.assertNotEqual(realestate["domain_orchestrator"],
                            automation["domain_orchestrator"])
        self.assertEqual(realestate["actual_nca_workers_started"],0)
        self.assertFalse(realestate["server_dispatch_authorized"])

    def test_19_unknown_domain_denied(self):
        with self.assertRaisesRegex(BridgeDenied,"UNKNOWN_FEDERATED_DOMAIN"):
            self.plan(domain="GLOBAL_GOD_ORCHESTRATOR")

    def test_20_unknown_lead_status_quarantined(self):
        proposal=self.plan(FakeDB(lead=[("NEW_UNCLASSIFIED_SOURCE",7)]))
        self.assertEqual(proposal["next_steps"][0]["gate"],"UNKNOWN_LEAD_STATE")

    def test_21_even_positive_payments_are_not_confirmed(self):
        db=FakeDB(totals={
            "registered_workspaces":3, "registered_agent_records":5,
            "payment_records":4,"revenue_ledger_entries":1})
        proposal=self.plan(db)
        self.assertIsNone(proposal["confirmed_payments"])
        self.assertIsNone(proposal["confirmed_revenue_minor"])
        self.assertIn("PAYMENT_RECONCILIATION",[x["kind"] for x in proposal["next_steps"]])

    def test_22_rejects_client_pii_injected_into_snapshot(self):
        snap=self.snapshot()
        snap["customer_email"]="someone@example.invalid"
        with self.assertRaisesRegex(BridgeDenied,"UNKNOWN_PRIVATE_SNAPSHOT"):
            draft_hanter_review(snap,now=STAMP)

    def test_23_rejects_fake_owner_authorization(self):
        snap=self.snapshot()
        snap["production_nca_dispatch_authorized"]=True
        with self.assertRaisesRegex(BridgeDenied,"UNSAFE_REPORTED_SOURCE_SCOPE"):
            draft_hanter_review(snap,now=STAMP)

    def test_24_proposal_never_leaves_private_boundary(self):
        p=self.plan()
        self.assertFalse(p["public_publishable"])
        self.assertFalse(p["personal_data_present"])
        self.assertFalse(p["ai_passport_verified"])
        self.assertFalse(p["approval_gateway_approved"])
        self.assertEqual(p["route_type"],"HANTER_REVIEW_PROPOSAL_ONLY")
        self.assertEqual(p["hanter_command_center"],"HANTER")
        self.assertEqual(len(p["planned_nca_roles"]),5)

    def test_25_timezone_required(self):
        with self.assertRaisesRegex(BridgeDenied,"OBSERVATION_REQUIRES_TIMEZONE"):
            inspect_counts(FakeDB(),observed_at=datetime(2026,11,3,8,30))

    def test_26_aggregate_size_limit(self):
        with self.assertRaisesRegex(BridgeDenied,"INVALID_AGGREGATE_COUNT"):
            self.snapshot(FakeDB(lead=[("NEEDS_QUALIFICATION",99_000_000)]))

    def test_27_no_silent_approval_from_manually_inserted_field(self):
        snap=self.snapshot()
        snap["owner_approved"]=True
        with self.assertRaises(BridgeDenied):
            draft_hanter_review(snap,now=STAMP)

    def test_28_no_tasks_can_be_sent_using_plan(self):
        plan=self.plan()
        self.assertFalse(plan["server_dispatch_authorized"])
        self.assertFalse(plan["guardian_core_approved"])
        self.assertFalse(plan["owner_approval_verified"])

    def test_29_no_code_credentials_required(self):
        self.assertFalse(hasattr(FakeDB(),"api_key"))
        plan=self.plan()
        self.assertNotIn("secret",str(plan).lower())

    def test_30_empty_aggregates_handled_without_fake_work(self):
        db=FakeDB(lead=[],task=[],totals={
            "registered_workspaces":0,"registered_agent_records":0,
            "payment_records":0,"revenue_ledger_entries":0})
        p=self.plan(db)
        self.assertEqual(p["next_steps"],[])
        self.assertEqual(p["actual_nca_workers_started"],0)


if __name__ == "__main__":
    unittest.main()
