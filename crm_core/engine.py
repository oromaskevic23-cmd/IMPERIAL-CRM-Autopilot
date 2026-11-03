"""CRM-SOFFT / Enterprise Deal Integrity: LOCAL SYNTHETIC REFERENCE ONLY.

Durable leads, federated 1+5 team planning, expiring mock leases, anti-replay,
independent mock QA, local kill gate, append-only checksums and NO booked money.
No signed AI Passport, authenticated tenant, provider, client or platform is
connected; this package MUST NEVER be used as a production authorizer.

Copyright (c) 2026 Alexander Nikolaevich Romaskevich (RomaskevicH).
"""
import hashlib
from contextlib import contextmanager
import json
from pathlib import Path
import re
import secrets
import sqlite3
import uuid

ROLES = {
    "AI_SERVICES": ("Intake Analyst","Solution Architect","Implementation NCA","Independent QA","Delivery Reviewer"),
    "FREELANCE": ("Opportunity Scout","Solution Architect","Builder","Independent QA","Delivery Reviewer"),
    "AUTOMATION": ("Workflow Analyst","Integration Architect","Sandbox Builder","Independent QA","Release Reviewer"),
    "REAL_ESTATE": ("Listing Researcher","Market Analyst","Document Analyst","Independent QA","Human-Licensed Handoff"),
    "BROKERAGE": ("Market Scout","Value Analyst","Due Diligence","Independent QA","Human-Licensed Handoff"),
    "DIGITAL_PRODUCTS": ("Market Scout","Product Architect","Constructor AI Builder","Independent QA","Release Reviewer")
}
IDENT = re.compile(r"[A-Za-z][A-Za-z0-9._:-]{1,79}\Z")
DIGEST = re.compile(r"[0-9a-f]{64}\Z")


class Denied(PermissionError):
    pass


def _id(value):
    if type(value) is not str or IDENT.fullmatch(value) is None:
        raise Denied("INVALID_IDENTIFIER")
    return value


def _proof(value):
    if type(value) is not str or DIGEST.fullmatch(value) is None:
        raise Denied("INVALID_EVIDENCE_DIGEST")
    return value


def _hash(value):
    return hashlib.sha256(value.encode("utf8")).hexdigest()


class DealEngine:
    """SQLite lab only: workspace ID is caller-supplied, not verified JWT/RLS."""

    def __init__(self, path):
        self.path = Path(path)
        if self.path.is_symlink():
            raise Denied("SYMLINK_DATABASE_DENIED")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._db() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS leads(
                  id TEXT PRIMARY KEY, workspace TEXT NOT NULL, source_key TEXT NOT NULL,
                  receipt TEXT NOT NULL, domain TEXT NOT NULL, title TEXT NOT NULL,
                  UNIQUE(workspace,source_key));
                CREATE TABLE IF NOT EXISTS cases(
                  id TEXT PRIMARY KEY, workspace TEXT NOT NULL, lead_id TEXT NOT NULL UNIQUE,
                  domain TEXT NOT NULL, orchestrator TEXT NOT NULL, state TEXT NOT NULL,
                  quote_minor INTEGER, currency TEXT);
                CREATE TABLE IF NOT EXISTS tasks(
                  id TEXT PRIMARY KEY, workspace TEXT NOT NULL, case_id TEXT NOT NULL,
                  role TEXT NOT NULL, agent_ref TEXT NOT NULL, state TEXT NOT NULL,
                  worker TEXT, token_hash TEXT, expires INTEGER, result_sha TEXT,
                  review_sha TEXT, UNIQUE(case_id,role));
                CREATE TABLE IF NOT EXISTS stops(
                  scope TEXT NOT NULL, subject TEXT NOT NULL, reason TEXT NOT NULL,
                  PRIMARY KEY(scope,subject));
                CREATE TABLE IF NOT EXISTS audit(
                  seq INTEGER PRIMARY KEY AUTOINCREMENT, event TEXT NOT NULL,
                  prior TEXT NOT NULL, digest TEXT NOT NULL);
                CREATE TRIGGER IF NOT EXISTS audit_no_delete BEFORE DELETE ON audit
                BEGIN SELECT RAISE(ABORT,'audit-append-only'); END;
                CREATE TRIGGER IF NOT EXISTS audit_no_update BEFORE UPDATE ON audit
                BEGIN SELECT RAISE(ABORT,'audit-append-only'); END;
            """)

    @contextmanager
    def _db(self):
        db=sqlite3.connect(self.path,timeout=8)
        db.row_factory=sqlite3.Row
        db.execute("PRAGMA busy_timeout=8000")
        try:
            with db:
                yield db
        finally:
            db.close()

    def _audit(self,db,record):
        row=db.execute("SELECT digest FROM audit ORDER BY seq DESC LIMIT 1").fetchone()
        previous=row["digest"] if row else "0"*64
        event=json.dumps(record,sort_keys=True,separators=(",",":"),ensure_ascii=True)
        db.execute("INSERT INTO audit(event,prior,digest) VALUES(?,?,?)",
                   (event,previous,_hash(previous+"|"+event)))

    def _allowed(self,db,workspace,case=None):
        entries=[("global","*"),("workspace",workspace)]
        if case: entries.append(("case",case))
        if any(db.execute("SELECT 1 FROM stops WHERE scope=? AND subject=?",x).fetchone() for x in entries):
            raise Denied("STOP_ACTIVE")

    def intake(self,workspace,source_key,receipt,domain,title,now):
        _id(workspace);_id(source_key);_proof(receipt)
        if domain not in ROLES or type(title) is not str or not 4<=len(title)<=120 or any(c in title for c in "<>\x00"):
            raise Denied("INVALID_SYNTHETIC_SOURCE")
        if type(now) is not int or now<0: raise Denied("INVALID_TIME")
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE");self._allowed(db,workspace)
            prior=db.execute("SELECT id,receipt,domain,title FROM leads WHERE workspace=? AND source_key=?",
                             (workspace,source_key)).fetchone()
            if prior:
                if (prior["receipt"],prior["domain"],prior["title"])!=(receipt,domain,title):
                    raise Denied("SOURCE_CONFLICT")
                case=db.execute("SELECT id FROM cases WHERE lead_id=?",(prior["id"],)).fetchone()
                return {"lead_id":prior["id"],"case_id":case["id"],"duplicate":True}
            lead_id,case_id="LEAD-"+uuid.uuid4().hex,"CASE-"+uuid.uuid4().hex
            db.execute("INSERT INTO leads VALUES(?,?,?,?,?,?)",(lead_id,workspace,source_key,receipt,domain,title))
            db.execute("INSERT INTO cases(id,workspace,lead_id,domain,orchestrator,state) VALUES(?,?,?,?,?,?)",
                       (case_id,workspace,lead_id,domain,"LAB-FEDERATED-"+domain,"LAB_DISCOVERED"))
            self._audit(db,{"event":"LAB_INTAKE","workspace":workspace,"case":case_id,
                            "source_sha256":receipt,"at":now})
            return {"lead_id":lead_id,"case_id":case_id,"duplicate":False}

    def plan(self,workspace,case_id,now):
        _id(workspace);_id(case_id)
        if type(now) is not int or now<0:raise Denied("INVALID_TIME")
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE");self._allowed(db,workspace,case_id)
            case=db.execute("SELECT domain,state,orchestrator FROM cases WHERE workspace=? AND id=?",
                            (workspace,case_id)).fetchone()
            if not case or case["state"]!="LAB_DISCOVERED":raise Denied("NO_ELIGIBLE_CASE")
            for i,role in enumerate(ROLES[case["domain"]],1):
                db.execute("INSERT INTO tasks(id,workspace,case_id,role,agent_ref,state) VALUES(?,?,?,?,?,?)",
                           ("TASK-"+uuid.uuid4().hex,workspace,case_id,role,f"LAB-NCA-{i:03d}","LAB_PENDING"))
            db.execute("UPDATE cases SET state='LAB_PLANNED' WHERE id=?",(case_id,))
            self._audit(db,{"event":"LAB_SQUAD_PLANNED","case":case_id,"workspace":workspace,"at":now})
            return {"orchestrator":case["orchestrator"],"roles":list(ROLES[case["domain"]]),
                    "real_active_workers":0,"production_authorized":False}

    def claim(self,workspace,case_id,worker,now,lease=120):
        _id(workspace);_id(case_id);_id(worker)
        if type(now) is not int or type(lease) is not int or now<0 or not 1<=lease<=300:
            raise Denied("INVALID_LEASE")
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE");self._allowed(db,workspace,case_id)
            row=db.execute("SELECT t.id,t.role FROM tasks t JOIN cases c ON c.id=t.case_id "
                           "WHERE t.workspace=? AND t.case_id=? AND c.workspace=? "
                           "AND c.state='LAB_PLANNED' AND t.state='LAB_PENDING' ORDER BY t.rowid LIMIT 1",
                           (workspace,case_id,workspace)).fetchone()
            if row is None:return None
            token=secrets.token_hex(24)
            db.execute("UPDATE tasks SET state='LAB_CLAIMED',worker=?,token_hash=?,expires=? WHERE id=?",
                       (worker,_hash(token),now+lease,row["id"]))
            self._audit(db,{"event":"LAB_CLAIM","workspace":workspace,"task_id":row["id"],"at":now})
            return {"task_id":row["id"],"role":row["role"],"token":token,"expires":now+lease}

    def complete(self,workspace,task_id,worker,token,result_sha,review_sha,reviewer,now):
        _id(workspace);_id(task_id);_id(worker);_id(reviewer)
        _proof(result_sha);_proof(review_sha)
        if worker==reviewer or result_sha==review_sha:
            raise Denied("SEPARATE_LAB_REVIEW_REQUIRED")
        if type(token) is not str or type(now) is not int or now<0:
            raise Denied("INVALID_COMPLETION")
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            task=db.execute("SELECT * FROM tasks WHERE workspace=? AND id=?",
                            (workspace,task_id)).fetchone()
            if not task or task["state"]!="LAB_CLAIMED":raise Denied("TASK_NOT_CLAIMED")
            self._allowed(db,workspace,task["case_id"])
            if now>=task["expires"]:raise Denied("LEASE_EXPIRED")
            if task["worker"]!=worker or not secrets.compare_digest(task["token_hash"],_hash(token)):
                raise Denied("CLAIM_PROOF_REQUIRED")
            db.execute("UPDATE tasks SET state='LAB_QA_RECORDED',result_sha=?,review_sha=? WHERE id=?",
                       (result_sha,review_sha,task_id))
            self._audit(db,{"event":"LAB_QA_RECORDED","workspace":workspace,"task_id":task_id,
                            "result":result_sha,"review":review_sha,"at":now})
            return {"lab_qa_recorded":True,"independent_human_qa":False,
                    "client_accepted":False,"production_authorized":False}

    def quote(self,workspace,case_id,amount_minor,currency,now):
        _id(workspace);_id(case_id)
        if (type(amount_minor) is not int or not 0<amount_minor<=10**12
                or currency not in ("USD","EUR","GBP") or type(now) is not int or now<0):
            raise Denied("INVALID_QUOTE")
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE");self._allowed(db,workspace,case_id)
            case=db.execute("SELECT state FROM cases WHERE workspace=? AND id=?",
                            (workspace,case_id)).fetchone()
            if not case or case["state"]!="LAB_PLANNED":
                raise Denied("CASE_NOT_APPROVED_FOR_LAB_QUOTE")
            db.execute("UPDATE cases SET quote_minor=?,currency=? WHERE id=?",
                       (amount_minor,currency,case_id))
            self._audit(db,{"event":"LAB_QUOTE_NOT_REVENUE","case":case_id,
                            "amount_minor":amount_minor,"currency":currency,"at":now})
            return {"illustrative_quote_minor":amount_minor,
                    "confirmed_revenue_minor":None,"external_offer_sent":False}

    def confirm_payment(self,**kwargs):
        raise Denied("PROVIDER_RECONCILIATION_AND_APPROVAL_GATEWAY_NOT_CONNECTED")

    def send_offer(self,**kwargs):
        raise Denied("SIGNED_CLIENT_MANDATE_AND_APPROVAL_GATEWAY_REQUIRED")

    def stop(self,scope,subject,reason,now):
        if (scope not in ("global","workspace","case") or type(reason) is not str
                or not 4<=len(reason)<=150 or type(now) is not int or now<0):
            raise Denied("INVALID_STOP")
        if scope=="global" and subject!="*":raise Denied("INVALID_GLOBAL_STOP")
        if scope!="global":_id(subject)
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            db.execute("INSERT OR REPLACE INTO stops VALUES(?,?,?)",(scope,subject,reason))
            if scope=="global":
                db.execute("UPDATE tasks SET state='LAB_STOPPED' WHERE state IN ('LAB_PENDING','LAB_CLAIMED')")
            elif scope=="workspace":
                db.execute("UPDATE tasks SET state='LAB_STOPPED' WHERE workspace=? "
                           "AND state IN ('LAB_PENDING','LAB_CLAIMED')",(subject,))
            else:
                db.execute("UPDATE tasks SET state='LAB_STOPPED' WHERE case_id=? "
                           "AND state IN ('LAB_PENDING','LAB_CLAIMED')",(subject,))
            self._audit(db,{"event":"LOCAL_STOP","scope":scope,"subject":subject,"at":now})
            return {"local_stop_recorded":True,"remote_kill_verified":False}

    def summary(self,workspace):
        _id(workspace)
        with self._db() as db:
            n=db.execute("SELECT count(*) FROM leads WHERE workspace=?",(workspace,)).fetchone()[0]
            tasks=db.execute("SELECT state,count(*) n FROM tasks WHERE workspace=? GROUP BY state",
                             (workspace,)).fetchall()
            return {"source":"OFFLINE_SYNTHETIC_FIXTURE_ONLY","workspace":workspace,
                    "lab_leads":n,"lab_tasks_by_state":{r["state"]:r["n"] for r in tasks},
                    "real_active_workers":None,"confirmed_payments":None,
                    "confirmed_revenue_minor":None,"authenticated_runtime":False,
                    "production_authorized":False}

    def audit_valid(self):
        with self._db() as db:
            previous="0"*64
            for row in db.execute("SELECT event,prior,digest FROM audit ORDER BY seq"):
                if row["prior"]!=previous or row["digest"]!=_hash(previous+"|"+row["event"]):
                    return False
                previous=row["digest"]
        return True
