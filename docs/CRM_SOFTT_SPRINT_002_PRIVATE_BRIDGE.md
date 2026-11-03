# CRM-SOFFT — Sprint 002: Private Read-only Supabase Bridge × HANTER Review Routing

**Checkpoint:** 3 November 2026  
**Architecture owner:** Alexander Nikolaevich Romaskevich (RomaskevicH), Founder • Owner • CEO • Chief Systems Architect, Final Architectural Decision Authority.  
**Budget:** FREE_ONLY; no paid providers enabled.  
**Production status:** no production CRM bridge credentials or real HANTER dispatch have been activated.

## Delivered and independently observed

**A. Aggregate-only PostgreSQL bridge:**
- [`crm_bridge/readonly.py`](../crm_bridge/readonly.py) issues only six fixed, aggregate SELECT queries covering lead/task status counts and four non-personal record counts.
- Uses an explicit PostgreSQL read-only transaction and a 3-second statement timeout.
- Denies superuser and `BYPASSRLS` sessions, non-read-only transactions, unexpected labels, excessive row counts and missing credentials/connection.
- Returns **zero** raw lead details, names, source references, invoice identifiers, customer messages or payment evidence.
- A trusted, privately provisioned **least-privilege** database connection must be passed from a protected runtime; no actual Supabase connection token or password is contained in this repo. The code cannot deploy itself.

**B. HANTER review proposal, not command execution:**
- [`crm_bridge/triage.py`](../crm_bridge/triage.py) transforms fresh aggregates into a conservative review plan under HANTER and a **named federated domain orchestrator**. It never creates a global AI superuser.
- `RESEARCH_ONLY_NOT_A_VERIFIED_BUYER` remains research, `NEEDS_QUALIFICATION` requires accountable human review, `OUTREACH_SENT_WAITING_REPLY` cannot cause duplicate outreach, `BLOCKED` cannot dispatch, and unknown statuses go to manual classification.
- Any payment/ledger row count, even positive, is **not** proof of provider-backed settlement. Confirmed payment and recognized revenue stay **null**.
- No real NCA workers are launched; proposed five-agent team roles are **architecture only**, without signed AI Passport or approval.
- Both source aggregate and review proposal are **private**; neither is a safe public GitHub Pages payment feed.

**C. Tested evidence:**
- [Read-only guards and triage CI #41605063519](https://github.com/oromaskevic23-cmd/IMPERIAL-CRM-Autopilot/actions/runs/41605063519) — **30/30 PASS on Python 3.11 and 30/30 PASS on Python 3.12**.
- [Genuine isolated PostgreSQL 17 CI #41605467918](https://github.com/oromaskevic23-cmd/IMPERIAL-CRM-Autopilot/actions/runs/41605467918) — **30/30 guard tests and 3/3 actual PostgreSQL integration tests PASS**.
- PostgreSQL 17.11 in disposable GitHub Actions container returned aggregate counts under a non-superuser role and rejected an attempted `INSERT` with `permission denied for table lead_registry`. The integration uses **synthetic fixture records**, not the live Supabase database.

## Live Supabase findings (from separate authorized read-only review)

The current private Supabase instance already has `crm_sofft`, with 11 registered workspaces, 21 registered agent records, 14 lead records, 26 task records, zero `payment_records` and zero `revenue_ledger` entries in the checked tables. More detailed per-state counts and the RLS/GRANT security assessment are in the private governance repository; **no source identifiers or personal lead data are copied to public GitHub**.

The Supabase advisory reported 21 tables without RLS in the `imperial_crm` and `imperial_control` schemas, **but a separate direct permission check** found no direct `anon`/`authenticated` read or write grants on the tested capabilities for those tables. Do not claim real public exposure based only on the warning.

Many existing `crm_sofft` tables have RLS enabled but currently lack compatible RLS policies for ordinary clients; a non-bypass reporting role may be unable to see rows even after `GRANT SELECT`. **Do not weaken RLS or add unconditional `USING(true)` to fix this.** An approved private reporting scope and negative tenant-isolation tests are required first.

## Running in development

All policy tests use Python standard library and **synthetic fake DB responses**:

```bash
python3 -m unittest discover -s tests -p 'test_crm_bridge.py' -v
```

True PostgreSQL contract verification uses a disposable localhost PostgreSQL container and pinned [Psycopg 3](../crm_bridge/requirements-postgres-ci.txt); see [the isolated workflow](../.github/workflows/crm-bridge-postgres.yml). Its synthetic credentials belong only to the ephemeral CI service and never connect to Supabase.

**External runtime contract (NOT yet deployed):** a privately authenticated, non-superuser, non-BYPASSRLS PostgreSQL role must be granted access to an approved tenant-aware aggregate projection. The runtime injects an already-established `psycopg.Connection` into `inspect_counts(connection)` and passes the resulting **private** snapshot to `draft_hanter_review(snapshot)`. Credentials must reside only in a protected vault. Never embed a service-role key or connection DSN in the browser, Notion, NCA prompt, public README or GitHub Actions.

## Required gates before real dispatch or commercial claims

1. **Database access:** approved reporting identity, audited exact grants, tenant-scoped RLS/policies and negative cross-workspace isolation checks; no dangerous RLS blanket change.
2. **Verified individual mandate:** one real lead must have consent, source provenance, lawful platform rights and explicit workspace owner approval; aggregate counts are insufficient to select or contact any individual.
3. **Signed command chain:** Architect → HANTER → relevant **federated orchestrator** → one scoped NCA with true AI Passport, Guardian Core, Approval Gateway and IntentLock. No simulated role may execute actual work.
4. **Independent QA:** professional LEGION examiner and documented deliverable acceptance, not a second synthetic hash.
5. **Actual owner-controlled stop:** protected remote Owner Kill Switch must terminate active agents with test evidence, not merely mark an SQLite row.
6. **Commercial ledger:** external provider confirmation, client invoice/contract reference, beneficiary and currency reconciliation, idempotency, refund/chargeback tracking and tamper-resistant Audit Ledger before `PAYMENT_CONFIRMED`.
7. **Audit and operator UX:** private dashboard for reviewed leads and approvals; public GitHub Pages may display only approved, sanitized aggregates, never raw customer or payment data.

Keep CRYPTO IMPERIAL Ecosystem Boundary separate. IMPERIUM is a **long-term architectural global digital currency vision for AI agents**, not a statement of present worldwide use or financial market status.

**Architecture Before Implementation → Implementation Before Evidence → Evidence Before Privileged Commercial Execution.**
