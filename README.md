# IMPERIAL-CRM-Autopilot

**Enterprise AI-native multi-industry CRM, federated task orchestration and evidence-first commercial operations.**

Founder • Owner • CEO • Chief Systems Architect: **Alexander Nikolaevich Romaskevich** — **RomaskevicH**.

## IMPERIAL Core: CRM-SOFFT NCA release authority — Sprint 003

**Implementation focus: our own IMPERIAL Core operating system, not competitors.** [Fail-closed production-readiness gate](crm_control/release_gate.py) · [26 adversarial tests](tests/test_crm_release_gate.py) · [Architecture and production requirements](docs/CRM_SOFTT_SPRINT_003_NCA_RELEASE_GATE.md) · [GitHub Actions 26/26 PASS on Python 3.11/3.12](https://github.com/oromaskevic23-cmd/IMPERIAL-CRM-Autopilot/actions/runs/41685910346).

The new control gate explicitly **DENIES** actual NCA dispatch, customer outreach, payment confirmation, private data publication and Owner role transfer until external trusted authorizations are independently verified. Even an all-green self-reported status document cannot promote an agent to production. The demonstration is synthetic and there is **no active HANTER production worker** implied.

A separate read-only audit of our real Supabase `crm_sofft` database found 21 agent records still `REGISTERED_NOT_AUTHORIZED`, 11 workspaces `CONFIGURING`, and no payment/revenue rows in the checked tables. A private, non-identifying aggregate snapshot was committed to the **private** IMPERIAL Core governance repository. No real customer records, payment details, passports or credentials are published here.

## New: CRM-SOFFT Private Read-only Bridge × HANTER review — Sprint 002

[Fixed-query PostgreSQL bridge](crm_bridge/readonly.py) · [Fail-closed HANTER triage](crm_bridge/triage.py) · [Enterprise specification](docs/CRM_SOFTT_SPRINT_002_PRIVATE_BRIDGE.md) · [30/30 Python 3.11 and 3.12 CI](https://github.com/oromaskevic23-cmd/IMPERIAL-CRM-Autopilot/actions/runs/41605063519) · [Real isolated PostgreSQL 17 proof](https://github.com/oromaskevic23-cmd/IMPERIAL-CRM-Autopilot/actions/runs/41605467918).

**Verified results:** 30/30 aggregate-query and adversarial routing tests PASS on each supported Python version; in a separate disposable PostgreSQL 17 instance, three actual SQL integration tests PASS, including a **database-level rejection of an unauthorized INSERT**. HANTER receives only a review proposal; no signed Owner command, customer outreach, real agent or payment is issued.

**Live Supabase is NOT connected to this new runtime adapter.** Existing CRM-SOFFT data was inspected independently using read-only privileged project tooling. A suitable private reporting identity, tenant-scoped RLS policies and protected Owner/Approval Gateway controls must exist before activating the adapter on production. No client records, credentials or private runtime snapshots are committed here.

## New: CRM-SOFFT Deal Integrity & Federated Dispatch — verified 3 November 2026

[Working Python/SQLite laboratory engine](crm_core/engine.py) · [Executable one-shot pilot](crm_core/__main__.py) · [22 adversarial unit tests](tests/test_crm_core.py) · [Enterprise sprint specification](docs/CRM_SOFTT_SPRINT_001_DEAL_INTEGRITY.md) · [GitHub Actions proof](https://github.com/oromaskevic23-cmd/IMPERIAL-CRM-Autopilot/actions/runs/41602727818).

**Real verification:** **22/22 PASS on Python 3.11 and 22/22 PASS on Python 3.12**, including a complete *synthetic* lead → domain-orchestrator → five NCA role plans → leased task → lab QA receipt → persisted stop cycle. Run `python3 -m unittest discover -s tests -p 'test_crm_core.py' -v` and `python3 -m crm_core` from the repo root; no paid API, cloud account or dependency installation required.

The money boundary is strict: `confirm_payment` and `send_offer` **reject all calls** until an authenticated customer mandate, Guardian Core, Approval Gateway, independent QA and trusted payment-provider reconciliation are integrated. Illustrative quotes cannot become `PAYMENT_CONFIRMED` revenue. The local database is not the production `crm_sofft` schema, callers are not authenticated tenants, and mock roles are not active agents.

**Live Supabase note:** a separate read-only review confirmed existing CRM-SOFFT records but found security configuration requiring a staged private policy audit. No live database permissions, customers, tasks or payments were changed by this sprint. A protected remediation runbook is stored in the private IMPERIAL Core governance repository, not exposed publicly.

## What is implemented
- Responsive, mobile-first **IMPERIAL CRM Command Deck**, written as first-party HTML, CSS and JavaScript in [site/](site/).
- Real, read-only public **GitHub API telemetry**: stars, forks, open tracker count, latest commit and latest GitHub Actions result. Client refresh approximately every five minutes, subject to network availability and GitHub rate limits.
- Configurable **design scenarios** for universal 1-orchestrator + 5-NCA teams spanning multiple market cities in freelance, brokerage and real estate.
- Explicit **unconnected** server/NCA/payment metrics in [site/data/runtime-status.json](site/data/runtime-status.json). The browser does NOT invent running workers, real deals or revenue.
- Strict browser Content Security Policy, no client secrets or control-plane writes, independent source validation in [scripts/check_dashboard.py](scripts/check_dashboard.py).
- GitHub Actions validation and Pages deployment workflow at [.github/workflows/pages.yml](.github/workflows/pages.yml).

**Important:** A deployed dashboard is not a deployed CRM backend. The page never claims that a million agents, autonomous trading/brokerage, real client contracts, or provider-confirmed payments are operational.

## Architecture
Read [Enterprise Architecture v1.0](docs/ARCHITECTURE.md) for the proposed implementation:
- HANTER command center → multiple federated domain/region orchestrators → Nano Core Agents.
- CRM-SOFFT multi-workspace architecture: freelance, brokerage, real estate, AI services, automation, digital products and more.
- Autonomous **authorized** lead discovery → qualification → Approval Gateway → NCA task execution → independent QA → client acceptance → provider-backed payment verification.
- AI Passport, Enterprise Skills, Guardian Core, ProofGraph, Audit Ledger, Zero Trust and Owner Kill Switch.
- A **million NCA logical identities** as a scale architecture goal, NOT a current worker fleet count.
- Distinct **CRYPTO IMPERIAL Ecosystem Boundary**, financial ledgers and data privacy boundaries.

## GitHub Pages
The deployment workflow validates and publishes only the public site directory. Once GitHub Pages has been enabled with **GitHub Actions** as the publishing source in repository settings, the intended Pages URL is:

https://oromaskevic23-cmd.github.io/IMPERIAL-CRM-Autopilot/

Check [workflow runs](https://github.com/oromaskevic23-cmd/IMPERIAL-CRM-Autopilot/actions) to confirm actual deployment. The Pages URL is not considered verified until a successful run and a working public response have been observed.

## Local check
Run in the repository root:

    python3 scripts/check_dashboard.py
    node --check site/assets/dashboard.js

For a local static preview:

    python3 -m http.server 8000 --directory site

Then visit http://localhost:8000. Local/Pages mode shows public GitHub data; the NCA and payment feed remains disconnected until a secured production projection exists.

## Engineering priorities
1. Implement private, tenant-isolated CRM storage, permissioned connectors and real approved lead ingestion.
2. Connect one registered, signed AI Passport worker and an actual domain orchestrator, with independent QA and reversible execution.
3. Deliver the first **authorized real customer case** with complete evidence.
4. Add payment provider reconciliation, server-derived aggregates and independently reviewable telemetry.
5. Progress through performance and security scale gates before any large-fleet availability claim.

**Security:** Never put provider credentials, customer information, signed permits or unrestricted agent controls into public GitHub Pages. The public dashboard is a **read-only observability layer**.

**Attribution:** Original IMPERIAL Core architecture and code contributions must preserve authorship records. No organizational incorporation, production service operation or legal exclusivity is implied by this repository.
