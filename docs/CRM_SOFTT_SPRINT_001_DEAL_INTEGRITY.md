# CRM-SOFFT — Enterprise Deal Integrity & Federated Dispatch · Sprint 001

**Checkpoint:** 3 November 2026  
**Authority:** Alexander Nikolaevich Romaskevich (RomaskevicH) — Founder • Owner • CEO • Chief Systems Architect, Final Architectural Decision Authority.  
**Budget:** FREE_ONLY.  
**Current maturity:** executed offline synthetic commercial workflow, validated on GitHub Actions. **NOT** a deployed authenticated CRM backend, operating commercial autopilot or payment service.

## Why this sprint

Existing IMPERIAL CRM Autopilot has a well-designed public observational dashboard and a proposed federated architecture, but lacked a tested backend command/ledger boundary. This sprint adds a **self-contained Python 3.11+ SQLite implementation** in [crm_core](../crm_core/engine.py) and a reproducible no-network test runner. No customer records are stored in the public repository or static GitHub Pages.

**Verified proof:** [GitHub Actions run 41602727818](https://github.com/oromaskevic23-cmd/IMPERIAL-CRM-Autopilot/actions/runs/41602727818): **22/22 tests PASS** in Python 3.11 and **22/22 PASS** in Python 3.12, including actual SQLite transactions, lease expiry, replay/idempotency control, cross-workspace denial, local stop, QA separation and explicit payment denial.

## Canonical architecture and business boundaries

Architect → HANTER (AI Command Center) → **federated domain- and region-specific orchestrators** → specialized Nano Core Agents (NCA) → isolated execution. HANTER does not become a global omnipotent orchestrator. Keep ORION, LEGION, VELION (MAX is one mode), CONSTRUCTOR AI, CRM-SOFFT, AI Passport, Enterprise Skills, Guardian Core, Approval Gateway, IntentLock, Audit Ledger, ProofGraph, Zero Trust, Public/Private Boundary and Owner Kill Switch.

The CRYPTO IMPERIAL Ecosystem Boundary is separate from customer commerce and fiat settlement. IMPERIUM is only a **long-term architectural digital currency vision for AI agents worldwide**, not a claim of real current global monetary adoption, price, exchange listing or settled CRM income.

## Implemented local workflow (all LAB states)

1. **Intake:** ingest one explicitly synthetic source receipt identified by a SHA-256 digest. Scope by workspace and deduplicate by `(workspace, source_key)`. An attempt to change the same source's digest requires manual review.
2. **Case:** atomically bind source → case → domain-specific federated orchestrator in a durable SQLite transaction. No prompt alone can create a signed mandate.
3. **Squad:** generate exactly five specialized **role placeholders**, never a claim of real running NCA. Workflows exist for AI Services, Freelance, Automation, Real Estate, Brokerage and Digital Products. Regulated industry templates require licensed human handoff.
4. **Leases:** a local worker can claim one pending role task with a one-time random token and deadline, up to five minutes. Claim state is persisted; parallel claims cannot silently select the same row.
5. **QA:** output and a separate lab-review digest must differ; the reviewer ID must differ from the worker ID. Record the receipt while explicitly declaring `independent_human_qa = false`. A digest difference does not by itself prove professional competence.
6. **Local stop:** persistent global, workspace or case stop blocks new actions and prevents an in-flight worker from registering a completion. A local stop does not automatically terminate remotely running worker processes.
7. **Quote:** any proposed amount is recorded in integer **minor currency units** and classified only as an **illustrative laboratory quote**. Quotes, invoices, forecasts and opportunity scores are not recognized revenue.
8. **Money trust gate:** `confirm_payment` and `send_offer` are **hard denied**. The system has no authenticated customer mandate, trusted payment-provider events, Approval Gateway or independent reconciliation. It never asserts `PAYMENT_CONFIRMED`.

## Acceptance evidence

| Verification | Observed result | Truth boundary |
| --- | --- | --- |
| Python 3.11 | 22/22 PASS | Actual SQLite local lab |
| Python 3.12 | 22/22 PASS | Actual SQLite local lab |
| Synthetic lead → case → squad | PASS | Five roles, zero real NCA workers |
| Deduplication and workspace scoping | PASS | Caller-supplied IDs not authenticated JWT |
| Persistent stop / token claim / lease expiration | PASS | One local host; not remote Owner Kill Switch |
| Separate QA digest | PASS | Not independently authenticated human QA |
| Quote vs confirmed payment isolation | PASS | No verified provider payment |
| Append-only audit hash chain | PASS | Local SQLite administrator can still alter schema/DB |
| Real lead sourcing / payment / deployment | NOT EXECUTED | No client contact or service account enabled |

## Reproduce without dependencies

From repository root, Python 3.11 or later:

```bash
python3 -m unittest discover -s tests -p 'test_crm_core.py' -v
python3 -m crm_core
```

Both use synthetic in-memory ideas and a temporary local database; neither needs an API key, cloud provider, browser, trained model, payment account or recurring job. The CLI reports null confirmed revenue and payments, and never prints an invented success for external work.

## Required before real commercial deployment

**Gate A — protect source data.** Enroll a private HANTER runtime identity and trust/tenant directory, bind incoming sources to an actual platform-approved provider API or an opted-in customer. No unauthorized marketplace account scraping, fake listings, credential/cookie extraction or unsolicited outreach.

**Gate B — enforce database tenancy.** Use the existing private `crm_sofft` schema in Supabase and keep private client records outside GitHub Pages. Verify exposed schemas, grants and RLS; implement authenticated workspace membership, independent service identity and negative IDOR/BOLA tests, not caller-supplied workspace labels. Current production schema must be audited before changing grants or policies.

**Gate C — signed orchestration.** Route one actual HANTER task to a *specific* federated orchestrator and one NCA holding a version-bound AI Passport. Enforce Guardian Core and Approval Gateway on every external action; restrict per-mission skills, browser and cloud connectors.

**Gate D — professional independent QA.** LEGION examiner performs unseen test assignment; independent review validates deliverable identity, client scope, security and SLA before handoff. A self-declared QA hash is insufficient.

**Gate E — payment settlement evidence.** A real payment provider signs/webhooks a transaction, with verified payer/beneficiary, amount, currency, timestamp, invoice/task linkage, duplication checks, refunds and compensating ledger entries. Use `PAYMENT_CONFIRMED` only after separate trusted reconciliation. Store no card/payment credentials in public logs.

**Gate F — controlled hosting.** Deploy one managed free-tier worker only with an authorized protected runtime, secret vault and measured stop/rollback, then independently verify. GitHub Actions CI and public Pages do not constitute 24/7 NCA execution. Do not provision paid resources.

## Related artifacts

- [Existing Enterprise architecture](ARCHITECTURE.md)
- [Full Python implementation](../crm_core/engine.py)
- [Adversarial tests](../tests/test_crm_core.py)
- [CI](../.github/workflows/crm-core.yml)
- [Safe public dashboard](../site/index.html)

**Architecture Before Implementation → Implementation Before Evidence → Evidence Before Commercial Claims.**
