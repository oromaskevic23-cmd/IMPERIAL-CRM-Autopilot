"""Real PostgreSQL 17 integration proof against a TEMPORARY CI-ONLY database.

Not the user's Supabase. Requires explicit ephemeral CI environment variable,
localhost only, and a synthetic DB credential provided by GitHub Actions.
No real business records, payments, or agent sessions are accessed.
"""
from datetime import datetime, timezone
import json
import os
import unittest

from crm_bridge.readonly import inspect_counts
from crm_bridge.triage import draft_hanter_review


class PostgresIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.environ.get("IMPERIAL_CRM_LOCAL_PG_CI")!="ISOLATED_EPHEMERAL_ONLY":
            raise RuntimeError("Refusing non-isolated PostgreSQL integration run")
        if os.environ.get("PGHOST") not in ("127.0.0.1","localhost"):
            raise RuntimeError("Database must run on the local ephemeral CI host")
        import psycopg
        cls.psycopg=psycopg
        cls.conn=psycopg.connect(
            host="127.0.0.1",port=5432,dbname="postgres",user="postgres",
            password=os.environ["PGPASSWORD"],connect_timeout=8,
            autocommit=True)
        statements=[
            "CREATE SCHEMA crm_sofft",
            "CREATE ROLE crm_ci_reader NOLOGIN NOSUPERUSER NOBYPASSRLS",
            "CREATE TABLE crm_sofft.lead_registry (state text NOT NULL)",
            "CREATE TABLE crm_sofft.task_registry (state text NOT NULL)",
            "CREATE TABLE crm_sofft.workspace_registry (workspace_id text NOT NULL)",
            "CREATE TABLE crm_sofft.agent_registry (agent_id text NOT NULL)",
            "CREATE TABLE crm_sofft.payment_records (payment_status text NOT NULL)",
            "CREATE TABLE crm_sofft.revenue_ledger (entry_id text NOT NULL)",
            "INSERT INTO crm_sofft.lead_registry VALUES "
            "('NEEDS_QUALIFICATION'),('RESEARCH_ONLY_NOT_A_VERIFIED_BUYER'),"
            "('RESEARCH_ONLY_NOT_A_VERIFIED_BUYER'),('OUTREACH_SENT_WAITING_REPLY')",
            "INSERT INTO crm_sofft.task_registry VALUES ('DRAFT'),('DRAFT'),('BLOCKED')",
            "INSERT INTO crm_sofft.workspace_registry VALUES ('SYNTHETIC-A'),('SYNTHETIC-B')",
            "INSERT INTO crm_sofft.agent_registry VALUES ('SYNTHETIC-NCA')",
            "GRANT USAGE ON SCHEMA crm_sofft TO crm_ci_reader",
            "GRANT SELECT ON ALL TABLES IN SCHEMA crm_sofft TO crm_ci_reader",
        ]
        for stmt in statements:
            cls.conn.execute(stmt)
        cls.conn.execute("SET ROLE crm_ci_reader")

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls,"conn"):
            cls.conn.close()

    def test_actual_postgres_read_only_aggregation(self):
        self.assertEqual(self.conn.execute("SELECT current_user").fetchone()[0],
                         "crm_ci_reader")
        stamp=datetime.now(timezone.utc)
        record=inspect_counts(self.conn,observed_at=stamp)
        self.assertEqual(record["lead_states"]["NEEDS_QUALIFICATION"],1)
        self.assertEqual(record["lead_states"]["RESEARCH_ONLY_NOT_A_VERIFIED_BUYER"],2)
        self.assertEqual(record["task_states"]["BLOCKED"],1)
        self.assertEqual(record["totals"]["registered_workspaces"],2)
        self.assertEqual(record["totals"]["registered_agent_records"],1)
        self.assertEqual(record["totals"]["payment_records"],0)
        self.assertFalse(record["database_write_performed"])

    def test_actual_postgres_rejects_writes(self):
        from psycopg.errors import InsufficientPrivilege
        with self.assertRaises(InsufficientPrivilege):
            self.conn.execute("INSERT INTO crm_sofft.lead_registry VALUES ('FORGED_APPROVED')")

    def test_real_sql_transaction_stays_fail_closed(self):
        snap=inspect_counts(self.conn,observed_at=datetime.now(timezone.utc))
        plan=draft_hanter_review(snap,now=datetime.now(timezone.utc),domain="FREELANCE")
        self.assertEqual(plan["route_type"],"HANTER_REVIEW_PROPOSAL_ONLY")
        self.assertEqual(plan["hanter_command_center"],"HANTER")
        self.assertEqual(plan["actual_nca_workers_started"],0)
        self.assertFalse(plan["server_dispatch_authorized"])
        self.assertIsNone(plan["confirmed_payments"])
        self.assertFalse(plan["public_publishable"])
        print(json.dumps({
            "verification":"EPHEMERAL_POSTGRESQL_REAL_SQL_PASS",
            "postgres_version":self.conn.execute("SHOW server_version").fetchone()[0],
            "roles":"NON_SUPERUSER_READ_ONLY",
            "synthetic_leads":sum(snap["lead_states"].values()),
            "synthetic_tasks":sum(snap["task_states"].values()),
            "real_supabase_connected":False,
            "real_client_records_read":0,
            "commercial_actions":0,
            "real_worker_started":0,
            "production_authorized":False
        },sort_keys=True))


if __name__ == "__main__":
    unittest.main()
