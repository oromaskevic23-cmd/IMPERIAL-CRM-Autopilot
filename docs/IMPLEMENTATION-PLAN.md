# IMPERIAL-CRM-Autopilot — Implementation Plan and Release Gates

**Status:** Proposed plan, not an implementation report.  
**Execution principle:** Architecture -> Implementation -> Independent Verification -> Evidence -> Expansion.  
**Initial cost policy:** FREE_ONLY; paid infrastructure or transactions require a separate explicit Owner authorization.

## 0. Current evidence checkpoint (2026-11-02)

- GitHub repository exists, with a short introductory README.
- This proposed design branch adds architecture, operating model and release plan documents.
- No verified deployed API, authenticated worker, authorized source integration, actual marketplace deal, paid invoice, reconciled payment, five-NCA end-to-end execution, or million-agent capacity is established by these documents.
- No production readiness percentage should be inferred from repository description or design completeness.
- Existing IMPERIAL Core assets (HANTER, CRM-SOFFT, VELION, ORION, LEGION, CYBER HAK) are intended dependencies; their individual current runtime status must be independently checked prior to integration.

## 1. Release R0 — Truthful runnable foundation

**Goal:** One tenant / one workspace / one mission can run safely in a controlled sandbox.

Deliverables:
- API service with authentication, JWT/session validation, typed mission endpoints.
- PostgreSQL schema/migrations and integration tests of tenant isolation (RLS).
- Durable job queue with idempotency keys, per-job lease, retry and dead-letter state.
- Local/approved model adapter; no hidden dependence on credentials stored in repo.
- Agent registry, roles, immutable skill proof and mock AI Passport in TEST mode.
- Real cryptographic AI Passport verification required for any non-test executor.
- Guardian Core enforcement policy, mocked dangerous action denied, Approval Gateway, Owner Kill Switch.
- Audit Ledger and immutable evidence manifest.
- Minimal CI: lint, unit tests, integration tests, secret scan, dependency scan.

**Release gate:** independently replay one sandbox job, prove deny/allow and kill switch; all RLS cross-tenant tests PASS; exact run IDs stored.

## 2. Release R1 — First real approved commercial opportunity

**Goal:** One source -> one signed mission -> one five-NCA pod -> a verifiable deliverable.

Deliverables:
- One approved API or an owned inbound lead form (not an unauthorized scraper).
- Opportunity deduplication, source provenance and lead policy.
- Mission router HANTER -> one federated domain orchestrator -> team orchestrator -> five NCAs.
- A work-order contract with milestones and accept/reject rules.
- Independent QA and recorded approval to deliver.
- Human-reviewed offer template, contract status and authorized customer communication.
- Genuine execution by an authenticated persistent worker using a permitted LLM.
- Financial state machine with PAYMENT_PENDING by default.

**Release gate:** one end-to-end allowed, reproducible real-world or approved pilot task with independent PASS; client acceptance/contract evidence where applicable. A real payment is reported only after external confirmation.

## 3. Release R2 — Distributed multi-city operations

**Goal:** Five NCAs coordinated across city/timezone assignments on one deal, with lawful jurisdiction coverage.

Deliverables:
- City Deal Atlas, geographies, jurisdiction rules and partner registry.
- Team Factory with skill and region matching.
- Human handoff, language/location scheduling and conflict management.
- Real-estate support pack behind a licensing/representation policy gate.
- B2B brokerage pack separate from property brokerage.
- Versioned regulatory policies reviewed for each initial operating jurisdiction.
- Structured work handoffs, optimistic locking and task-lease takeover.
- Quality analytics with transparent denominator counts.

**Release gate:** cross-city simulated work plus at least one authorized low-risk pilot, with complete audit proofs and an explicit record of any human professionals involved.

## 4. Release R3 — Multi-industry business fabric

**Goal:** At least three fully isolated domain packs over one CRM core.

Deliverables:
- Freelance, B2B services and real estate support (or other approved) packs.
- Independent domain orchestrators and namespace/queue isolation.
- Tenant-specific budgets, quotas, provider rate limits and fair scheduling.
- Customer 360, deal room, support case, contract and document management.
- Verified payment provider integration and ledger reconciliation where lawful and authorized.
- Incident response and recovery exercises.
- Observability metrics (saturation, errors, latency, backlog, cost, fraud signals).

**Release gate:** prove no cross-tenant/industry authorization bypass; independently QA each domain; reconcile a test or authorized actual payment without fictitious status.

## 5. Release R4 — Million-agent design readiness

**Goal:** Demonstrate control-plane capacity in staging before claiming scale.

Deliverables:
- Synthetic registration and policy evaluation for **1,000,000 NCA identity records** (capacity target, not active workers).
- Sharded/partitioned agent registry, cursor-based listing and asynchronous work dispatch.
- Bounded concurrency/load shedding and backpressure tests.
- Multiple independent work queues and domain orchestrators.
- Explicit budgets per tenant, user, team, mission and connector.
- Incremental fault injection, active/passive failover and recovery-time evidence.
- Cost projection for N active workers vs N registered identities.
- Security/revocation exercises at registration scale.

**Release gate:** publish hardware/region configuration, dataset, throughput, p50/p95/p99 latency, failed operations, cost and reproducible load-test results; never label the test 1M workers if it was 1M records.

## 6. Proposed service layout

~~~text
apps/
  control-dashboard/          # CRM, mission, City Deal Atlas, money, security views
  operator-console/           # Architect/HANTER controls
services/
  crm-api/                    # Organization/workspace/customer/opportunity boundaries
  hanter-gateway/             # Command intake and federated dispatch
  domain-freelance/           # Freelance orchestrator
  domain-brokerage/           # Brokerage orchestrator
  domain-real-estate/         # Property support orchestrator
  team-orchestrator/          # Pod assignment/handoffs
  opportunity-ingestion/      # Authorized connectors only
  agent-registry/             # Passport, skills, leases
  nca-worker/                 # Isolated, authorized execution
  guardian-policy/            # Zero Trust policy checks
  approval-gateway/           # Approval binding, revocation
  qa-service/                 # Independent verification
  finance-ledger/             # Invoices, external payment proofs
  audit-ledger/               # Append-only event proofs
  connector-registry/         # Provider allowlist, permitted scopes
packages/
  contracts/                  # Versioned events and API schemas
  domain-packs/               # Industry policies and templates
  enterprise-skills/          # Skill definitions and exams
  security-controls/          # Shared auth and cryptographic verification
  ui-components/              # Shared design system
infra/
  migrations/                 # Postgres/Supabase migration source
  deployment/                 # Reproducible container manifests
  observability/              # Metrics and alert rules
tests/
  contract/
  integration/
  cross-tenant/
  security/
  e2e/
  load/
docs/
  ARCHITECTURE.md
  OPERATIONS-PLAYBOOK.md
  IMPLEMENTATION-PLAN.md
~~~

This is a proposed layout. Listed paths are not evidence that those services already exist. Domain names are canonical and must not be arbitrarily renamed.

## 7. Proposed SLOs (targets, not measured facts)

| Metric | Proposed initial target | Evidence |
| --- | --- | --- |
| Unauthorized external paid actions | 0 | Gateway-denial integration tests |
| Cross-tenant data access | 0 | RLS/auth integration tests |
| Duplicate external submits | 0 | Idempotency test + provider event trail |
| Unverified payments recorded as confirmed | 0 | Ledger invariants and negative tests |
| Mission audit coverage | 100% for controlled execution | Manifest completeness audit |
| Independent QA before external delivery | 100% for enforced work classes | QA decision records |
| Kill Switch revocation test | PASS | Signed permit denied after revocation |
| First real NCA mission | 1 reproducible accepted mission | Evidence bundle |
| Million registered agents | PLANNED | Staging load-test evidence only |

Do not publish aspirational SLOs as achieved service levels.

## 8. Test matrix

- **Authorization:** missing, expired, forged and revoked passport; wrong organization; wrong permitted skill; replayed approval.
- **Queue:** worker crash mid-task; lease expiry; two concurrent claimants; duplicate events; retry exhaustion.
- **Data:** row-level isolation; secret exposure; unauthorized export; PII retention policy; deletion request.
- **Platform:** rate-limit 429; connector revoked; platform response schema changes; terms not approved.
- **QA:** the executing NCA attempting self-approval; failure after deliverable generation; unsafe output.
- **Finance:** duplicate webhook; forged event; wrong currency; partial payment; refunded payment; chargeback; no source proof.
- **Brokerage:** no licensed local professional; cross-jurisdiction conflict; unsuitable representation; unclear counterparty identity.
- **Kill switch:** pause while work in flight; reject new leases, permits and outbound actions; preserve forensic trail.
- **Disaster:** database unavailable; evidence store unavailable; orchestrator restart; recovery from durable events.

## 9. Prioritized immediate implementation backlog

1. Repository governance: CODEOWNERS, branch protection recommendation, CI and protected documentation review.
2. Typed contracts and shared database migrations: organizations -> opportunity -> mission -> task -> evidence.
3. Runtime worker and dispatcher running in a sandbox with deterministic sample mission.
4. Real Agent Passport enforcement, Guardian Core, Approval Gateway and Kill Switch.
5. Independent QA with external proof manifest.
6. One authorized opportunity connector or owned inbound form.
7. Full five-agent end-to-end pilot, quality gates and cost accounting.
8. City Deal Atlas and one jurisdiction-controlled partner workflow.
9. Third-party payment reconciliation only when authorized credentials and relevant legal/contract obligations are fulfilled.
10. Load/scale testing and multi-industry rollout behind measurable readiness gates.

## 10. Governance and ownership

Architecture authority remains with Founder • Owner • CEO • Chief Systems Architect Alexander Nikolaevich Romaskevich. Preserve author attribution and commit history; do not misrepresent legal corporate registration, registered trademarks, licensing or commercial capacity. Keep secrets and private customer data outside public repositories.

Architecture changes require documented decision records, backwards compatibility analysis and independent review. High-risk runtime actions must be policy-gated regardless of who initiates the instruction.
