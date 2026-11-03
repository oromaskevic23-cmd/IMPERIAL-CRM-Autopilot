"""Real SQLite and business-boundary tests for synthetic CRM-SOFFT Core."""
import hashlib
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
import unittest

from crm_core.engine import DealEngine, Denied


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


class CRMCoreTests(unittest.TestCase):
    def setUp(self):
        temp=TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.path=Path(temp.name)/"crm.db"
        self.crm=DealEngine(self.path)

    def lead(self,workspace="AI-SERVICES",key="lead001",domain="AI_SERVICES"):
        return self.crm.intake(workspace,key,digest("synthetic source"),domain,
                               "Synthetic workflow request",100)

    def planned(self):
        lead=self.lead()
        squad=self.crm.plan("AI-SERVICES",lead["case_id"],101)
        return lead,squad

    def test_01_intake_is_synthetic_and_audited(self):
        result=self.lead()
        self.assertFalse(result["duplicate"])
        self.assertTrue(self.crm.audit_valid())
        self.assertIsNone(self.crm.summary("AI-SERVICES")["confirmed_revenue_minor"])

    def test_02_idempotent_ingestion(self):
        original=self.lead()
        duplicate=self.lead()
        self.assertEqual(original["case_id"],duplicate["case_id"])
        self.assertTrue(duplicate["duplicate"])
        self.assertEqual(self.crm.summary("AI-SERVICES")["lab_leads"],1)

    def test_03_conflicting_duplicate_is_rejected(self):
        self.lead()
        with self.assertRaisesRegex(Denied,"SOURCE_CONFLICT"):
            self.crm.intake("AI-SERVICES","lead001",digest("changed"),"AI_SERVICES",
                            "Synthetic workflow request",101)

    def test_04_workspace_scoping_and_unique_cases(self):
        a=self.lead()
        b=self.lead(workspace="AUTOMATION")
        self.assertNotEqual(a["case_id"],b["case_id"])
        self.assertEqual(self.crm.summary("AUTOMATION")["lab_leads"],1)

    def test_05_one_domain_orchestrator_five_roles(self):
        case,squad=self.planned()
        self.assertEqual(len(squad["roles"]),5)
        self.assertEqual(squad["orchestrator"],"LAB-FEDERATED-AI_SERVICES")
        self.assertEqual(squad["real_active_workers"],0)
        self.assertFalse(squad["production_authorized"])
        self.assertEqual(self.crm.summary("AI-SERVICES")["lab_tasks_by_state"]["LAB_PENDING"],5)

    def test_06_duplicate_squad_does_not_double_task(self):
        case,_=self.planned()
        with self.assertRaisesRegex(Denied,"NO_ELIGIBLE_CASE"):
            self.crm.plan("AI-SERVICES",case["case_id"],102)

    def test_07_real_estate_human_licensed_handoff(self):
        lead=self.lead(domain="REAL_ESTATE")
        team=self.crm.plan("AI-SERVICES",lead["case_id"],101)
        self.assertIn("Human-Licensed Handoff",team["roles"])

    def test_08_cross_workspace_case_denied(self):
        lead,_=self.planned()
        with self.assertRaises(Denied):
            self.crm.plan("AUTOMATION",lead["case_id"],102)
        self.assertIsNone(self.crm.claim("AUTOMATION",lead["case_id"],"LAB-WORKER",103))

    def test_09_claim_issues_unique_bounded_task(self):
        lead,_=self.planned()
        first=self.crm.claim("AI-SERVICES",lead["case_id"],"LAB-WORKER",103)
        second=self.crm.claim("AI-SERVICES",lead["case_id"],"LAB-WORKER-2",103)
        self.assertNotEqual(first["task_id"],second["task_id"])
        self.assertEqual(first["expires"],223)

    def test_10_review_cannot_be_by_same_worker(self):
        lead,_=self.planned()
        claim=self.crm.claim("AI-SERVICES",lead["case_id"],"LAB-WORKER",103)
        with self.assertRaisesRegex(Denied,"SEPARATE_LAB_REVIEW"):
            self.crm.complete("AI-SERVICES",claim["task_id"],"LAB-WORKER",claim["token"],
                              digest("result"),digest("review"),"LAB-WORKER",104)

    def test_11_valid_lab_review_does_not_imply_human_qa(self):
        lead,_=self.planned()
        claim=self.crm.claim("AI-SERVICES",lead["case_id"],"LAB-WORKER",103)
        result=self.crm.complete("AI-SERVICES",claim["task_id"],"LAB-WORKER",claim["token"],
                                 digest("result"),digest("review"),"LAB-REVIEWER",104)
        self.assertTrue(result["lab_qa_recorded"])
        self.assertFalse(result["independent_human_qa"])
        self.assertFalse(result["production_authorized"])

    def test_12_double_completion_is_denied(self):
        lead,_=self.planned()
        claim=self.crm.claim("AI-SERVICES",lead["case_id"],"LAB-WORKER",103)
        args=("AI-SERVICES",claim["task_id"],"LAB-WORKER",claim["token"],
              digest("result"),digest("review"),"LAB-REVIEWER")
        self.crm.complete(*args,104)
        with self.assertRaisesRegex(Denied,"TASK_NOT_CLAIMED"):
            self.crm.complete(*args,105)

    def test_13_stolen_claim_proof_denied(self):
        lead,_=self.planned()
        claim=self.crm.claim("AI-SERVICES",lead["case_id"],"LAB-WORKER",103)
        with self.assertRaisesRegex(Denied,"CLAIM_PROOF_REQUIRED"):
            self.crm.complete("AI-SERVICES",claim["task_id"],"OTHER-WORKER",claim["token"],
                              digest("result"),digest("review"),"LAB-REVIEWER",104)
        with self.assertRaisesRegex(Denied,"CLAIM_PROOF_REQUIRED"):
            self.crm.complete("AI-SERVICES",claim["task_id"],"LAB-WORKER","WRONG-TOKEN",
                              digest("result"),digest("review"),"LAB-REVIEWER",104)

    def test_14_expired_lease_cannot_complete(self):
        lead,_=self.planned()
        claim=self.crm.claim("AI-SERVICES",lead["case_id"],"LAB-WORKER",103,lease=1)
        with self.assertRaisesRegex(Denied,"LEASE_EXPIRED"):
            self.crm.complete("AI-SERVICES",claim["task_id"],"LAB-WORKER",claim["token"],
                              digest("result"),digest("review"),"LAB-REVIEWER",104)

    def test_15_persisted_stop_invalidates_active_work(self):
        lead,_=self.planned()
        claim=self.crm.claim("AI-SERVICES",lead["case_id"],"LAB-WORKER",103)
        self.crm.stop("case",lead["case_id"],"Local test shutdown",104)
        reopened=DealEngine(self.path)
        with self.assertRaises(Denied):
            reopened.complete("AI-SERVICES",claim["task_id"],"LAB-WORKER",claim["token"],
                              digest("result"),digest("review"),"LAB-REVIEWER",105)
        self.assertEqual(reopened.summary("AI-SERVICES")["lab_tasks_by_state"]["LAB_STOPPED"],5)
        self.assertTrue(reopened.audit_valid())

    def test_16_global_stop_denies_intake(self):
        self.crm.stop("global","*","Local global freeze",90)
        with self.assertRaisesRegex(Denied,"STOP_ACTIVE"):
            self.lead()

    def test_17_workspace_stop_has_narrow_scope(self):
        self.crm.stop("workspace","AI-SERVICES","Local pause",90)
        with self.assertRaises(Denied):
            self.lead()
        self.assertFalse(self.lead(workspace="AUTOMATION")["duplicate"])

    def test_18_quote_is_not_confirmed_money(self):
        lead,_=self.planned()
        quote=self.crm.quote("AI-SERVICES",lead["case_id"],125000,"USD",110)
        self.assertEqual(quote["illustrative_quote_minor"],125000)
        self.assertIsNone(quote["confirmed_revenue_minor"])
        self.assertFalse(quote["external_offer_sent"])
        self.assertIsNone(self.crm.summary("AI-SERVICES")["confirmed_payments"])

    def test_19_payment_and_outreach_fail_closed(self):
        with self.assertRaisesRegex(Denied,"PROVIDER_RECONCILIATION"):
            self.crm.confirm_payment(provider="demo",status="confirmed")
        with self.assertRaisesRegex(Denied,"SIGNED_CLIENT_MANDATE"):
            self.crm.send_offer(email="nobody@example.invalid")

    def test_20_invalid_money_and_evidence_denied(self):
        lead,_=self.planned()
        for amount,currency in ((12.5,"USD"),(True,"USD"),(100,"BTC"),(-100,"EUR")):
            with self.subTest(amount=amount,currency=currency):
                with self.assertRaises(Denied):
                    self.crm.quote("AI-SERVICES",lead["case_id"],amount,currency,110)
        with self.assertRaises(Denied):
            self.crm.intake("AI-SERVICES","new","not-a-hash","AI_SERVICES","Synthetic",111)

    def test_21_audit_cannot_be_rewritten(self):
        self.lead()
        connection=sqlite3.connect(self.path)
        try:
            with self.assertRaises(sqlite3.DatabaseError):
                connection.execute("UPDATE audit SET event='{}' WHERE seq=1")
        finally:
            connection.rollback()
            connection.close()
        self.assertTrue(self.crm.audit_valid())

    def test_22_unknown_domain_rejected(self):
        with self.assertRaises(Denied):
            self.crm.intake("AI-SERVICES","lead001",digest("source"),
                            "UNAUTHORIZED_DOMAIN","Synthetic request",100)


if __name__=="__main__":
    unittest.main()
