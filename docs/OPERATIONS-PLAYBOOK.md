# Universal NCA Team Operations — Cross-City Playbook v1.0

**Status:** DESIGN SPECIFICATION. Examples are illustrative, not records of real customers, payments or licensed broker relationships. **Owner authority:** Alexander Nikolaevich Romaskevich.

## 1. Why a pod is not tied to one city

A five-NCA pod is an execution unit with one accountable team orchestrator, one mission, one task ledger and reproducible evidence. A geographic market (where the customer or asset resides), an agent's assigned coverage region (what market it understands), and a server execution region (where code runs) are separate concepts.

**Illustrative team:**
- Scout: New York market coverage.
- Analyst: Frankfurt market coverage.
- Commercial: London market coverage.
- Executor: Singapore market coverage.
- Deal Manager: Tokyo market coverage.
- Team Orchestrator: logical service operating in a permitted cloud region.
- Independent QA: a reviewer service outside the pod.

The pod can handle a permitted opportunity in a sixth city if its jurisdictional rules, language requirements, partner permissions, cross-border data rules and capacity permit it. Do not assume the pod members have any legal license based on their assigned cities.

## 2. NCA Team Factory and team assignment

Each job contains:
- industry pack and sub-type, customer and workspace;
- geographic market, jurisdiction and permitted data region;
- required hard skills and independently verified certifications;
- quality target, maximum cost, deadline and approval policy;
- privacy classification, platform channel and external action permissions.

Candidate teams must satisfy **hard gates first**: tenant isolation, identity validity, skills, jurisdiction permission, account entitlement, capacity, budget, no conflicted roles, and owner restrictions. Only among eligible teams rank by expected quality, available capacity, language, time-to-delivery, verified past results, and total cost. Never override legal compliance for a better score.

Assignment model:
- Shared mission workspace with mission_id, deal_id, work_order_id and immutable evidence references.
- Decomposition into typed, dependency-aware tasks; check state before advancing.
- Optimistic version checking prevents two agents from silently overwriting the same record.
- Leased tasks plus heartbeat; lease expiration causes re-queue and human-visible incident if required.
- Idempotency keys on every external action; bounded retries and dead-letter queues.
- Handoffs use structured artifacts and acceptance criteria, not only conversational summaries.
- Cross-timezone 24/7 execution is achieved through duty windows and standby capacity where funded, never by assuming one agent or chat is always running.

## 3. Industry playbooks

| Industry | Discover | Qualify | Execute | Mandatory independent gate |
| --- | --- | --- | --- | --- |
| Freelance software | Authorized platform API/inbound lead | Scope, budget, skill, fraud and platform policy | Sandbox code, tests, secure delivery | Independent QA + client approval |
| Graphic/content services | Permissioned brief intake | Rights, brand usage, source provenance, scope | Produce licensed original materials | Rights/privacy QA + client sign-off |
| B2B commercial matchmaking | Opt-in sources/referrals | Authority, conflicts, legal boundaries | Research and human-approved introduction | Compliance + counterparty verification |
| Real estate support | Allowed public listings/authorized partner feeds | Address, seller authorization, broker license and jurisdiction | Market reports, scheduling, document preparation | Licensed responsible professional where required |
| Service marketplace | Authorized inquiries | Coverage, provider credentials, budget | Appointment and coordination | Customer consent and provider verification |
| Digital product business | Owned storefront/inbound | Customer intent, terms, payments | Authorized product fulfillment | Delivery proof + payment verification |
| Enterprise sales | Approved CRM leads | Fit, consent, priority, account ownership | Personalized draft and sales handoff | Anti-spam policy + human approval as required |

## 4. Money and contract control

Opportunity forecast is a hypothesis, never cash. Separate accounting dimensions:
- quoted amount;
- customer-authorized contract amount;
- invoiced amount;
- payment due;
- externally confirmed captured/settled amount;
- refunds, chargebacks, platform commission and transfer fees;
- reconciled net amount;
- operational expenses and contribution margin.

Lifecycle: opportunity -> quote -> human-approved proposal -> customer acceptance -> binding agreement (where legally appropriate) -> work order -> independent QA -> approved delivery -> invoice -> trusted payment event -> reconciliation.

A bank/PSP platform integration must validate webhook signatures when supported, verify the provider object state against its API, deduplicate provider events, match customer/order/amount/currency and record source evidence. Bank transfer confirmations require authoritative statement/transaction evidence. PAYMENT_CONFIRMED must never be set by a language model alone.

No automatic deposits, crypto transactions, orders, refunds, legal contracts, broker commissions, transfers, margin borrowing or paid API usage without explicit permissions and applicable legal reviews.

## 5. Owner and human operations

- **Architect:** ultimate strategy, permission budget, emergency stop and final architecture decisions.
- **HANTER:** routing, operational command intake, cross-domain incidents and evidence aggregation.
- **Domain Orchestrator:** domain-specific policy, queue, team selection, SLA and mission controls.
- **Team Orchestrator:** coordinated subtasks, handoffs, retries, local team capacity.
- **Guardian Core:** action policy adjudication and risk scores.
- **Approval Gateway:** binding approval to subject, action hash, scope, TTL and authenticated owner decision.
- **Independent QA:** objective pass/fail with traceable evidence; must not be the work performer.
- **CYBER HAK:** audits and incident detection, not a replacement for legal compliance.
- **Audit Ledger:** independent append-only event history.
- **ORION:** research/recommendations without implied authority to commit.
- **VELION:** governed reasoning/model routing; no automatic claim of current model weights or runtime.
- **LEGION:** skill training, simulation, examinations and certification management.

Every agent must be suspendable or revocable through signed identity governance; emergency shutdown must be testable end-to-end.

## 6. Operator dashboard — proposed views

1. **Global Command:** eligible vs blocked missions, incidents, agent capacity, Owner approvals.
2. **Commercial Radar:** fresh authorized opportunities, platform provenance, predicted margin confidence.
3. **City Deal Atlas:** market/city coverage, verified partner status, deal stages, license gates.
4. **Pod Control:** assigned agents, active tasks, leases, QA status, delays.
5. **Customer 360:** contacts, consent, communications, obligations, contractual scopes.
6. **Money Control:** invoices, collected/reconciled cash, refunds, receivables, profitability.
7. **Agent Academy:** skill versions, exam runs, certification and revocation.
8. **Evidence Console:** signed manifests, audit replay, test failures, reproducibility.
9. **Security & Privacy:** blocked actions, RLS results, secret health, cross-tenant boundaries.
10. **Provider Connectors:** approved scopes, terms review dates, last success and errors.

### Mandatory dashboard integrity

Display aggregate counters **only from underlying database events**, and distinguish:
- registered identity vs active worker;
- business opportunity vs booked agreement;
- invoice vs confirmed payment;
- QA pass vs owner-approved release;
- configured connector vs actually functional connector.

Use explicit badges such as PLANNED, NOT CONFIGURED, BLOCKED, TESTED or LIVE, backed by recent evidence.

## 7. Useful alert triggers

- Provider revoked API permission or exceeded permitted rate.
- Mission/lease stalled beyond SLO.
- Required human approval is about to expire.
- No QA verdict before release.
- Reconciliation mismatch or negative net margin.
- Jurisdiction or human license validation missing.
- Critical security event; sensitive data exposure; failed cross-tenant check.
- Suspicious duplicated proposal, contact or property listing.

Alerts should be routed to a server-backed event inbox and optionally approved messaging connectors, with deduplication and anti-alert-storm rules. This design does not create a background service on its own.

## 8. Three end-to-end acceptance scenarios

### A. Freelance, software

Input: a permitted customer order to implement a small application.
Expected: authenticated source -> qualified work order -> five-agent assignment -> sandbox implementation -> independent code/tests QA -> Owner/client approval as required -> authorized delivery -> invoice -> payment pending until trustworthy provider evidence -> financial reconciliation.

### B. Real-estate support, cross-city

Input: a permitted partner request for comparable listings in a metropolitan area.
Expected: data-source provenance and usage permissions -> jurisdiction analysis -> property comparison -> privacy review -> licensed-human handoff where needed -> explicit customer sign-off -> separately validated fee if contract allows. The agents do **not** act as licensed brokers.

### C. Safety and money

Input: an NCA attempts to send an unapproved paid proposal or record an invented payment.
Expected: Guardian Core DENY -> Approval Gateway cannot be bypassed -> action is not executed -> Audit Ledger includes incident -> payment remains PENDING -> Owner Kill Switch can suspend the whole team without losing forensic evidence.

## 9. Competition on verifiable execution

Do not claim superiority over unnamed competitor systems without empirical data. Prove quality through measured first-pass QA, accepted deliverables, time from legitimate lead to delivery, false-positive/fraud detection, client retention, verified revenue and security incident rates. Publish a reproducible test harness and transparent metrics before external performance claims.
