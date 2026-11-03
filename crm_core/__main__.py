"""Reproducible one-shot offline synthetic CRM demonstration."""
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from .engine import DealEngine


def digest(text):
    return hashlib.sha256(text.encode("utf8")).hexdigest()


def main():
    with TemporaryDirectory(prefix="imperial-crm-lab-") as folder:
        crm=DealEngine(Path(folder)/"crm.db")
        lead=crm.intake("AI-SERVICES","lab-001",digest("synthetic-public-request"),
                        "AI_SERVICES","Synthetic automation request",100)
        squad=crm.plan("AI-SERVICES",lead["case_id"],101)
        quote=crm.quote("AI-SERVICES",lead["case_id"],120000,"USD",102)
        task=crm.claim("AI-SERVICES",lead["case_id"],"LAB-WORKER-001",103)
        qa=crm.complete("AI-SERVICES",task["task_id"],"LAB-WORKER-001",task["token"],
                        digest("synthetic-output"),digest("separate-lab-review"),"LAB-REVIEWER-002",104)
        stopped=crm.stop("case",lead["case_id"],"Lab emergency stop drill",105)
        print(json.dumps({
            "status":"OFFLINE_SYNTHETIC_CRM_ONLY",
            "federated_orchestrator":squad["orchestrator"],
            "role_count":len(squad["roles"]),
            "lab_qa_receipt":qa["lab_qa_recorded"],
            "quote_not_revenue":quote["confirmed_revenue_minor"] is None,
            "local_stop_recorded":stopped["local_stop_recorded"],
            "audit_hash_chain_valid":crm.audit_valid(),
            "summary":crm.summary("AI-SERVICES"),
            "real_client_jobs":0,"real_provider_payment_confirmations":0,
            "real_agent_inference":False,"real_external_actions":0
        },sort_keys=True,indent=2))


if __name__=="__main__":
    main()
