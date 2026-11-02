# IMPERIAL-CRM-Autopilot

**Enterprise AI-native multi-industry CRM, federated task orchestration and evidence-first commercial operations.**

Founder • Owner • CEO • Chief Systems Architect: **Alexander Nikolaevich Romaskevich** — **RomaskevicH**.

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
