# IMPERIAL-CRM-Autopilot — Enterprise Architecture v1.0

**Status:** PROPOSED / DESIGN ONLY — no production deployment, autonomous execution, marketplace access, broker licenses, payment processing, or million-agent capacity is implied by this document.

**Architecture authority:** Alexander Nikolaevich Romaskevich — Founder • Owner • CEO • Chief Systems Architect, IMPERIAL Core.  
**Canonical approach:** Architecture Before Implementation; federated Multi-Orchestrator Architecture; Evidence Before Claims; Zero Trust; FREE_ONLY until explicitly authorized otherwise.  
**Repository language:** English.  
**Copyright notice (original architecture text):** Copyright © 2026 Alexander Nikolaevich Romaskevich. All rights reserved unless an explicit applicable license says otherwise. Third-party dependencies retain their own terms.

## 1. Executive architecture decision

IMPERIAL-CRM-Autopilot is a multi-tenant, multi-industry operational CRM and governed autonomous work platform. It connects customer relationships, opportunities, distributed professional agent teams, production execution, independent verification, contracts, and evidence-based revenue into one business control plane.

It is NOT a single worldwide CRM robot, an unlimited always-on scraper, an autonomous unlicensed brokerage service, or a wallet that assumes money has arrived.

The system is composed of independent business-domain orchestrators, reusable Nano Core Agents (NCA) and Enterprise Skills, controlled by HANTER as the AI Command Center and by the Architect through Owner Authority controls.

### Canonical architecture (logical, not deployed)

~~~text
                           ARCHITECT / OWNER AUTHORITY
                         Strategy | Approvals | Kill Switch
                                      |
                       HANTER — AI Command Center
                     Command intake | Routing | Evidence
                                      |
            +-------------------------+------------------------+
            |                         |                        |
   Freelance Orchestrator    Brokerage Orchestrator   Real Estate Orchestrator
            |                         |                        |
      Freelance Teams             Deal Teams               City Deal Teams
            |                         |                        |
            +-------------- Federated Work Mesh ---------------+
                             |                 |
                   Universal NCA Pods    CRM-SOFFT Workspaces
                             |                 |
                   VELION Model Engine    Opportunity / Customer
                   LEGION Agent Academy   Contract / Order Ledger
                   ORION Intelligence     Revenue / Case Ledger
                             |
                Independent QA / ProofGraph
                             |
           Guardian Core -> Approval Gateway -> Executor
                             |
                        Audit Ledger

  Across all planes: AI Passport | Enterprise Skills | CYBER HAK |
  Zero Trust | Policy Engine | Public/Private Boundary |
  CRYPTO IMPERIAL Ecosystem Boundary | Owner Kill Switch
~~~

HANTER is a command and coordination authority, not an all-purpose global execution orchestrator. Each domain orchestrator is independently versioned, quota-limited, and auditable. A team orchestrator coordinates an individual pod or mission; it is not a substitute for the domain orchestrator.

## 2. Capability modules

| Capability | Primary responsibility | Primary artifacts |
| --- | --- | --- |
| CRM-SOFFT Workspace Fabric | Organizations, tenants, workspaces, customers, contacts, accounts, permissions | customer_id, organization_id, workspace_id |
| Opportunity Discovery | Policy-compliant lead intake from permitted APIs, feeds, customer referrals and manually supplied sources | opportunity_id, source_proof |
| Global City Deal Atlas | Geographic opportunity matching, city coverage, local partners, timezone routing | city_id, jurisdiction_id, coverage_status |
| Opportunity Intelligence | Relevance, budget confidence, fraud risk, estimated margin and next action | scorecard, risk_record |
| Federated Mission Router | HANTER dispatches signed missions to eligible orchestrators | mission_id, routing_decision |
| NCA Team Factory | Assemble five-agent or variable-size pods by skill, language, jurisdiction and availability | team_id, agent_assignments |
| Universal Enterprise Skills | Versioned professions, tools, exams, policies and sandbox tasks | skill_version, exam_proof |
| Work Order & Delivery | Contracts, scoped tasks, artifacts, milestones, SLA, revisions | work_order_id, deliverable_id |
| Brokerage Deal Room | Counterparty intelligence, document collection, permitted coordination, human broker assignment | deal_id, licensed_partner_id |
| Independent QA | Separate reviewer/check suite with independent evidence | qa_report_id, verdict |
| Approval Gateway | Risk-tiered human approval before sensitive, irreversible or externally consequential actions | approval_id |
| Financial Control Plane | Quotes, invoices, external payment event intake, reconciliation, revenue analytics | invoice_id, payment_evidence_id |
| Audit Ledger & ProofGraph | Immutable-append audit and linked execution evidence | event_id, proof_id |
| Command Dashboard | Agent fleet, business pipeline, SLOs, costs, incidents, revenue | verified KPIs |
| Connector Registry | Allowed platform APIs and scopes; policy/rate limits per provider | connector_id, consent_id |
| Privacy & Security | RLS, encryption, minimal scopes, secret vault, retention and data access audits | security_event_id |

Existing canonical CRM-SOFFT workspaces (IMPERIAL-GLOBAL, ASTRA-REVENUE, SHPAIZMAN-RU, AI-SERVICES, AUTOMATION, REAL-ESTATE, FREELANCE, DIGITAL-PRODUCTS, RECURRING-SERVICES, TASK-MARKET) should be supported through a workspace registry rather than becoming hard-coded branches.

## 3. Five-NCA distributed deal pod (illustrative)

A pod may include members assigned to five separate geographic markets while collaborating on one shared mission. Location is metadata and routing preference, not a mandatory place of agent execution.

- **NCA-SCOUT:** authorized sourcing, deduplication, provenance and freshness checks.
- **NCA-ANALYST:** feasibility, price/risk and jurisdiction checks, fraud signals.
- **NCA-COMMERCIAL:** drafts personalized offers, collects approvals, coordinates human negotiations.
- **NCA-EXECUTOR:** executes authorized technical/digital work or coordinates real-world specialists.
- **NCA-DEAL-MANAGER:** updates CRM, documents, milestones, status, customer communication drafts.
- **TEAM ORCHESTRATOR:** leases tasks, manages handoff, SLA, retries, escalation and team-level reporting.
- **INDEPENDENT QA:** external to the executing pod; cannot self-certify execution.

The five roles are example positions, not five permanently rigid agent types. Enterprise Skills allow role-switching only after independently passed exams. One NCA may have multiple skills but cannot bypass separation-of-duties checks.

Example: a permitted property opportunity in City A can be researched by SCOUT in Market B, analyzed by ANALYST in Market C, coordinated by COMMERCIAL in Market D, documented by DEAL-MANAGER in Market E, and taken to a separately authorized human broker in City A. The workflow remains one deal with one audit trail and jurisdiction-specific compliance gates.

## 4. Domain behavior

### 4.1 Freelance Autopilot

1. Collect jobs only through authorized APIs, allowed feeds, inbound leads or manual intake.
2. Normalize to one opportunity schema; store source, observed timestamp and platform permissions.
3. Deduplicate across accounts and platforms, flag fraud, estimate skills, delivery effort and margin.
4. Select the best eligible team by skill, capacity, deadline, cost budget and past verified quality.
5. Draft compliant, non-spam proposals; require account-owner approval when platform policy or risk requires it.
6. On customer acceptance, record contract and milestone; never infer acceptance from a submitted proposal.
7. Execute within sandbox with VELION/CONSTRUCTOR AI where appropriate.
8. Independent QA checks requirements, tests, content originality/security, and deliverable evidence.
9. Obtain required approvals; deliver through the authorized channel; handle revisions.
10. Update financial states only from provider-confirmed evidence and reconciliation.

**Important:** 24/7 refers to the server-side eligible connectors, scheduling, task queues and recovery. It does not authorize unapproved scraping, unsolicited bulk applications or prohibited automation.

### 4.2 Brokerage Autopilot

A single brokerage industry pack is insufficient. There must be a **brokerage subtype registry** (real estate, commercial partnerships, B2B introductions, permitted procurement, etc.) with separate jurisdiction-specific policies.

- Opportunity discovery and market intelligence can be automated where lawful.
- Verification of ownership, sanctions/fraud signals, permissions, counterparties and conflict-of-interest must be explicit.
- Regulated brokerage, licensed activities, negotiation, client representation, marketing claims, contract signing, payment handling and personal data transfers require policy-controlled human professionals and, where required, appropriate licenses.
- Every deal has an accountable legal human or organization and a local jurisdiction policy record.
- AI agents never claim licenses, pretend to be people, make binding representations, or independently close regulated deals.

### 4.3 Cross-industry extensions

Add domain packs without changing the CRM kernel: real estate support; professional services; digital product sales; recruitment where lawful; customer support; property service coordination; enterprise sales; affiliate/referral programs where permitted. Each pack defines workflows, agent exams, integration capabilities, evidence requirements and legal constraints.

## 5. Autonomous workflow and durable state

Suggested opportunity state machine:

~~~text
DISCOVERED -> SOURCE_VALIDATED -> QUALIFIED -> COMPLIANCE_CHECKED
-> PROPOSAL_DRAFTED -> APPROVED_TO_SEND -> SENT
-> CUSTOMER_ACCEPTED -> CONTRACT_VALIDATED -> IN_PROGRESS
-> QA_PENDING -> QA_PASSED -> APPROVED_TO_DELIVER -> DELIVERED
-> CUSTOMER_ACCEPTED_DELIVERY -> INVOICED -> PAYMENT_PENDING
-> PAYMENT_VERIFIED -> RECONCILED -> COMPLETED
~~~

At every transition enforce explicit preconditions, actor identity, idempotency key and time-stamped audit evidence. Include terminal states: REJECTED, BLOCKED, CANCELLED, EXPIRED and DISPUTED. Transitions may be paused for approval and retried safely, but may not silently skip guards.

**PAYMENT_VERIFIED** requires trusted PSP/bank/platform evidence, signature verification where available, matching amount/currency/order, status validation and no contradictory chargeback or reversal. **RECONCILED** requires ledger matching. Neither a client promise nor a generated invoice constitutes revenue. Maintain refunds, fees, disputes and FX separately.

### Signed mission envelope — proposed schema

~~~json
{
  "mission_id": "uuid",
  "organization_id": "uuid",
  "workspace_id": "uuid",
  "domain": "freelance",
  "orchestrator_id": "uuid",
  "team_id": "uuid",
  "task_id": "uuid",
  "jurisdiction": "ISO-3166-code",
  "required_skills": ["verified-skill-id"],
  "policy_version": "policy-version-id",
  "passport_subject": "agent-id",
  "approval_id": null,
  "max_budget_usd": 0,
  "deadline_utc": "ISO-8601",
  "idempotency_key": "unique-per-intended-action",
  "proof_refs": []
}
~~~

The envelope is an interface proposal, not a deployed or cryptographically signed message. Implement signing and independent verification at the execution boundary, not merely as a field in JSON. Never place secrets, full customer records or private keys in the envelope.

## 6. Agent identity, admissions and team membership

Every NCA must have:
- AI Passport and verifiable active authorization / expiry / revocation status.
- Tenant and mission scope, minimal allowed connectors, maximum spend and runtime quotas.
- Versioned skill certificates, evidence of independent exam, and safety restrictions.
- Signed execution permit bound to task, scope and expiration.
- Heartbeat / lease, retry budget, timeout, and non-reusable idempotency key.
- Kill/revoke path, including immediate inability to obtain new execution permits.

Lifecycle:

~~~text
REGISTERED -> TRAINING -> EXAMINED -> CERTIFIED -> AVAILABLE
-> LEASED -> WORKING -> QA -> AVAILABLE
           |                     |
           +-> SUSPENDED/REVOKED <-+
~~~

Certification is domain- and jurisdiction-specific. A generic programming exam does not authorize regulated brokerage. Legacy agents imported from other registries begin as UNVERIFIED until assessed.

## 7. Data architecture

Recommended canonical relational entities (separate by tenant and workspace):

organizations, workspaces, users, roles, memberships, customers, contacts,
accounts, opportunities, opportunity_sources, cities, jurisdictions,
business_domain_packs, policies, orchestrators, agent_passports,
agents, agent_skills, skill_exams, teams, team_memberships, missions,
tasks, task_attempts, artifact_refs, qa_reviews, approvals, contracts,
deal_rooms, counterparties, licensed_partners, invoices, payment_events,
reconciliation_entries, connector_consents, provider_credentials_refs,
audit_events, incidents, cost_ledger, outbox_events, inbox_dedup.

Use PostgreSQL/Supabase as the initial transactional source of truth only after verifying accessible environment and schema. Apply row-level security (RLS) to tenant-owned records, enforce authorization at API and DB layers, encrypt sensitive data, and keep secrets in an approved vault rather than in GitHub. The outbox pattern prevents a database state change from becoming disconnected from the associated job/event publication.

Separate:
- **Operational state:** mutable workflow tables with row version and concurrency checks.
- **Audit state:** append-only, externally verifiable events / hash-chain or anchored manifests.
- **Evidence state:** immutable object artifacts with hashes and restricted read policies.
- **Derived analytics:** reproducible metrics and materialized aggregations.

Establish explicit retention schedules, data subject access/deletion procedures, customer consent and regional residency requirements. Audit integrity and privacy deletion should be handled through documented cryptographic references/pseudonymization rather than unlawful indefinite data retention.

## 8. Runtime and scaling

**Small production seed:** one durable worker pool, one work queue, one database, separate QA runner, orchestrator services and dashboards. Use managed infrastructure only within approved budget.

**Growth:** separate queue partitions by tenant/domain/region, introduce fair scheduling, worker autoscaling and reserved capacity, independently scalable provider connectors, typed events, circuit breakers and dead-letter queues.

**Target: 1,000,000 registered NCA identities, NOT 1,000,000 concurrently running paid LLM workers.** A million-agent registry is a design capacity target and requires future load-test evidence. If all agents are organized in five-agent pods, that is a theoretical 200,000 pods, before orchestrator and independent QA capacity. Registrations, active agents, concurrent workers and completed jobs are four different metrics.

Allocate resources on demand with admission control:
- Global and tenant-specific in-flight limits.
- Token / provider / API call / budget quotas.
- Per-provider contract-aware rate limits and hard stop on provider permission changes.
- Mission isolation, state snapshots, safe retries, backpressure and graceful recovery.
- No automatic purchase of additional services without Owner approval.

A chat session cannot itself guarantee 24/7 uptime. Always-on operation requires a deployed external service, credentials, scheduler, monitoring and verifiable health evidence.

## 9. Security and approvals

**Guardian Core** evaluates each action against mission scope, skill, identity, jurisdiction, PII, financial exposure and allowed API use.

**Approval Gateway** requires explicit human approval for payment execution, binding documents, regulated representation, non-trivial financial commitments, new provider authorizations and other high-impact actions. Numeric approval challenges are acceptable only after authenticated binding to a specific request and anti-replay controls.

**CYBER HAK** controls security testing, secrets leakage, dependency risk, malicious input, prompt-injection defenses and incident response.

**Owner Kill Switch** revokes new permits and pauses pending jobs across federated orchestrators. Existing in-flight work must support checkpoint/cancellation. Break-glass override is logged.

**Public/Private Boundary:** public repo can contain architecture, schemas and test fixtures, not client PII, credentials, financial records or private implementations. **CRYPTO IMPERIAL Ecosystem Boundary:** no implicit linkage of payment ledgers with crypto wallets, and no automatic token issuance/trading. IMPERIUM is a long-term architectural digital currency concept for AI agents worldwide, not evidence of current worldwide adoption or market status.

## 10. Audit, QA and success metrics

Independent QA is assigned outside the executing agent's trust domain. For code use tests, static analysis, isolated execution and proof bundles; for commercial documents use facts, client acceptance criteria and applicable licensed-human sign-off. Agent-generated confidence alone is NOT a QA pass.

Minimum mission evidence: source provenance; permission to access; assignment; signed permit; task attempts; tool outputs hashes; test/QA results; approvals; deliverable manifest; customer acceptance; financial records if applicable.

Dashboard KPI definitions:
- Discovered = deduplicated legally sourced opportunities.
- Qualified = opportunities passing domain policy.
- Proposals sent = platform-confirmed submissions.
- Deals won = customer/contract evidence.
- Revenue realized = reconciled, non-reversed payment evidence.
- QA first-pass rate = independent PASS / independently reviewed deliveries.
- SLA attainment = on-time deliverables / committed deliverables.
- Agent utilization = active leased execution time / available authorized time.
- Net contribution = confirmed revenue - direct verified costs - refunds and fees (not speculative token value).
- Safety = denied actions, unauthorized attempts, critical incidents and revocations.

Report unknown values as UNKNOWN, blocked as BLOCKED, and unverified functions as NOT IMPLEMENTED. Never infer 100% readiness or payment confirmation from architecture documents.

## 11. External policy notes and non-negotiable constraints

- Upwork requires approved authorization for automation and warns against unauthorized bots/scraping and spam proposals. See https://support.upwork.com/hc/en-us/articles/43342677368467-Use-bots-and-other-automation-properly .
- Upwork's developer program has approval and use-case limitations: https://support.upwork.com/hc/en-us/articles/115015857647-How-to-request-an-API-key-from-Upwork .
- Freelancer.com provides a documented API and sandbox: https://developer.freelancer.com/ . This does not automatically authorize every use case.
- Real-estate licensing varies by jurisdiction; e.g. see https://www.nar.realtor/membership/licensing-for-real-estate-professionals for US state-level licensing requirements.
- The EU GDPR data-minimization and privacy-by-design principles are relevant when processing personal data: https://eur-lex.europa.eu/eli/reg/2016/679/oj .

All jurisdiction/platform rules are dynamic. A connector is disabled by default until permissions and current terms are verified for the intended operation.

## 12. Explicit acceptance conditions

No "AUTOPILOT LIVE" claim until there is evidence of ALL of:
1. Real deployed orchestrator endpoint plus identity-enforced mission routing.
2. Genuine signed AI Passport and independently validated executor permit.
3. A long-running worker with durable queue, lease expiry and safe retry.
4. One authorized source connector producing reproducible opportunity evidence.
5. A five-NCA pod completing an authorized end-to-end job.
6. An independent QA verdict and reproducible proof bundle.
7. Approval Gateway blocking an unapproved sensitive action.
8. Owner Kill Switch preventing further execution.
9. RLS tests showing cross-tenant isolation.
10. Payment events remaining PENDING unless verified by actual external evidence.

The first release should prove one paid or sandbox job *correctly*, not claim a fleet of one million agents exists.

## 13. Decision log

- **ADR-001:** Federated multi-orchestrator, not one global orchestrator.
- **ADR-002:** Dynamic Universal NCA teams with skill passports and independent QA.
- **ADR-003:** Opportunities are sourced only via permissioned connectors.
- **ADR-004:** Brokerage and real-estate industry packs are jurisdiction-gated.
- **ADR-005:** Evidence-based payments and reconciliation; no synthetic revenue.
- **ADR-006:** Register-first, activate-on-demand million-agent target.
- **ADR-007:** Zero Trust approval and immediate revocation boundaries.
- **ADR-008:** Public enterprise architecture separate from private runtime secrets.
