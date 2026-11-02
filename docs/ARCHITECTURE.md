# IMPERIAL CRM Autopilot — Federated Enterprise Architecture v1.0

**Status:** architectural specification + public GitHub telemetry dashboard. This is NOT evidence that the commercial autopilot, broker network, NCA workers, or payment backend is running.

**Authority:** Alexander Nikolaevich Romaskevich — Founder • Owner • CEO • Chief Systems Architect of IMPERIAL Core. Public authorship: RomaskevicH.

## Canonical operating model
Architect → HANTER (AI Command Center) → domain- and region-scoped federated orchestrators → Nano Core Agents (NCA) → execution and proof. This is a **federated Multi-Orchestrator Architecture**, not one global orchestrator.

Preserve and integrate the existing components: CRM-SOFFT, ORION, LEGION, VELION, CONSTRUCTOR AI, Enterprise Skills, AI Passport, Guardian Core, Approval Gateway, Audit Ledger, ProofGraph, IntentLock, Owner Kill Switch, Zero Trust, Public/Private Boundary, and CRYPTO IMPERIAL Ecosystem Boundary. MAX is a VELION mode, not a renamed model.

IMPERIUM represents a long-term architectural digital currency vision for AI agents worldwide. This does not assert present worldwide adoption or market status. Token ecosystems and any associated treasury are isolated from CRM customer funds and recognized revenue.

## Universal industry modules
| Workspace or vertical | Authorized acquisition | Professional workflow | Mandatory checkpoint |
| --- | --- | --- | --- |
| FREELANCE | Allowed marketplace APIs; client opt-in | Scope → build → independent QA → deliver | Client message / bid approval |
| BROKERAGE | Mandated partner feeds; lawful public information | Match → diligence → documented handoff | Licensed human, jurisdiction and contract review |
| REAL_ESTATE / CAPITAL_CORE | Listing APIs and authorized local sources | Comparable research → document checks → coordination | Licensed broker and legal review |
| AI_SERVICES | Consented inbound offers | VELION/AI execution → test → acceptance | Customer data and usage rights |
| AUTOMATION | Client-approved requests | Integration design → sandbox → deploy | Production write approval |
| DIGITAL_PRODUCTS | Permitted market signals | CONSTRUCTOR AI → independent QA → release | Store publishing and pricing |
| RECURRING_SERVICES | Existing client mandates | Monitoring → incident → renewal | Contract scope / billing |
| TASK_MARKET / WORK AI | Authorized work offers | Team assignment → execution → QA | Platform rules and contracts |

Each domain pack provides case schemas, connector permissions, risk rules, Enterprise Skills, examination requirements, SLA, audit requirements, and reconciliation mappings. Industry packs are independently versioned and can share infrastructure but not confidential tenant data.

## Squad topology: 1 orchestrator + 5 NCAs
One case has a domain orchestrator owning team assignment, dependencies, time zones, cost ceiling, escalation, and audit. Five specialized NCAs receive narrow scoped tasks and separate AI Passports. For freelance: scout, architect, builder, independent tester, delivery agent. For brokerage: opportunity scout, valuation analyst, document investigator, transaction coordinator, independent QA. For real estate: listing intake, local market analyst, document analyst, transaction coordinator, independent QA.

Agents may handle markets such as Frankfurt, London, Dubai, New York and Singapore within one team. City assignments are **market jurisdiction labels**, not assertions of physical personnel or currently active agents. Data residency, platform rights, and regulated-role boundaries remain local. Any licensed professional function or binding external deal requires an authorized human.

A single case ID, a durable shared dependency graph, evidence objects and event timestamps coordinate asynchronous members. An orchestrator can be reassigned; a task cannot be silently executed twice.

## 24/7 autopilot lifecycle
DISCOVERED → DEDUPED → ELIGIBLE → QUALIFIED → RISK_REVIEW → APPROVED → TEAM_ALLOCATED → EXECUTING → INDEPENDENT_QA → CLIENT_ACCEPTED → INVOICED → PAYMENT_CONFIRMED → CLOSED.

Transitions include explicit failure, retry, cancellation, refund, and human escalation paths. Each transition must append: event ID, tenant, case ID, event type, actor passport, policy version, causation ID, UTC timestamp, evidence reference and outcome. Duplicate submissions are prevented with idempotency keys and durable leases.

24/7 monitoring means authorized connectors and real hosted workers, respecting platform API limits, login and anti-bot rules. No credential scraping, CAPTCHA bypass, unsolicited spam, fake job acceptance, or unsanctioned marketplace bots. Outbound bids, external messages, agreements and payments require valid authority under Approval Gateway.

## Money and contract integrity
The financial domain separates opportunity forecast, accepted contract, invoicing, settlement pending, PAYMENT_CONFIRMED, fees, refunds and net realized revenue. Forecasts and invoice totals MUST NOT be displayed as earned payments. Confirmed transactions require a verifiable external provider record, amount, currency, beneficiary, invoice/contract linkage, reconciliation status and timestamps. Reversals create compensating ledger entries, never deletions.

Payments, wallet signing and privileged actions remain server-side, with scoped permissions and human approvals. The CRYPTO IMPERIAL boundary prevents conflation of tokens and customer commerce. Additional regulatory controls may be required by each jurisdiction.

## Backend blueprint (not yet deployed by this dashboard)
Private API gateway and tenant identity → HANTER routing → domain orchestrator services → durable queues → secured NCA workers and isolated tool sandboxes → independent QA → Approval Gateway → client delivery and provider reconciliation → Audit Ledger / ProofGraph.

Store tenant and case data in a private PostgreSQL/Supabase schema with correctly configured RLS and access tests, encrypted evidence storage, transactional outbox and append-only audit. Partition queues by tenant, business domain and region. Add retries, dead-letter queues, rate limits, scoped secrets, timeouts, cost ceilings, per-worker heartbeats, autoscaling, tracing, incident alerts, fail-safe and tested restore.

Candidate data entities: tenants, workspaces, regions, domain_packs, mandates, accounts, leads, cases, teams, orchestrators, agents, agent_passports, agent_skills, tasks, assignments, attempts, approvals, qa_results, deliverables, evidence_objects, contracts, invoices, payment_provider_events, ledger_entries, audit_events, incidents and kill_switch_events.

The scale goal of **one million logical NCA identities** is NOT an installed worker count. Five NCA roles per team mathematically allow up to 200,000 role sets, but not 200,000 proven concurrent teams. A million-agent architecture needs identity registries, regional sharding, queue partitions, admission control, worker reuse, cost modeling, capacity tests and independent safety review. Never allocate one always-on process per registered identity without demonstrated need.

## Public live dashboard and data provenance
GitHub Pages serves site/index.html, site/assets/dashboard.css, site/assets/dashboard.js. The browser directly fetches public repository/commit/Actions metadata from the GitHub API at roughly five-minute intervals; anonymous GitHub rate limits may apply. GitHub activity is NOT proof of NCA or monetary activity.

Optional server feed is site/data/runtime-status.json. Until an authenticated private producer publishes an approved, sanitized, auditable projection, its source is unconnected and all monetary and NCA fields are null. Production feed schema:
- schema_version = 1
- source = server-readonly-projection
- observed_at = an actual ISO-8601 UTC time
- metrics.active_nca_workers, metrics.verified_deliveries, metrics.confirmed_payments = nonnegative integer or null
- metrics.confirmed_revenue = number or null, with currency USD/EUR/GBP
- evidence_links = nonempty set of public reviewable evidence links
- payment_verification = provider-confirmed only upon independently reconciled proof
- payment_evidence_url = real externally verifiable HTTPS evidence URL if safe to publish

Browser freshness cutoff is 30 minutes; stale snapshots are hidden. A public browser CANNOT independently authenticate producer assertions. Build server-side signed provenance, source verification, tenant filtering, published-aggregate approval and an audit chain before interpreting runtime figures as externally confirmed. Never publish client PII, keys, invoices, confidential URLs or financial transactions in public JSON.

GitHub Pages is **not the secure CRM administration portal**. No write credentials, approval tokens, owner kill switch buttons, financial payment actions or private agent commands belong there.

## Acceptance gates (no invented PASS)
M0: static dashboard code + tests + Pages workflow; separately verify public URL and actual Actions outcome.
M1: backend identity, RLS isolation, durable queue, agent registry and independent access audit.
M2: owner Ed25519 enrollment, real AI Passport, HANTER → domain orchestrator → one VELION-powered worker, Guardian/Approval, independent QA and rollback/kill-switch exercise.
M3: one real authorized lead, one real 1+5 squad, professional deliverable independently accepted, auditable client handoff.
M4: one compliant brokerage/real-estate market pilot through authorized licensed human professionals.
M5: 10 → 100 → 1,000 → larger fleets with proven performance, cost, recovery, policy and security controls before capacity claims.

Keep author contribution history and original code attribution. Public GitHub visibility does not establish a legally incorporated entity or automatically confer intellectual-property protection. Licensing and authorship rights must be reviewed separately.
