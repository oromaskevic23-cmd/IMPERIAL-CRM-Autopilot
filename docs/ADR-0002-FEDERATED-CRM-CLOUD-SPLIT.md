# ADR-0002: Federated Cloud Placement for CRM-SOFFT

**Status:** PROPOSED — architecture and migration plan, **not deployed**  
**Date:** 2026-11-04  
**Authority:** Alexander Nikolaevich Romaskevich (RomaskevicH), Founder / Owner / CEO / Chief Systems Architect  
**Operational constraints:** FREE_ONLY; Architecture Before Implementation; no service-plan upgrade, payment, live customer-data transfer, or provider account provisioning without distinct authorized execution and verified backup.

## Problem and evidence

The current Supabase Free project has already exceeded its reference 500 MiB database quota. The largest contributors are worker runtime challenge and event histories, cron execution history, CRM task event evidence, and append-only action records. Current incident mitigation reduces **dispensable monitoring frequency**; it does not reclaim database storage. No offsite proof-preserving archive is established.

Past account suspension at another hosting service involved a bundled provider AI quota being re-exposed through a standalone OpenAI-compatible relay. This is a policy/compliance failure, distinct from capacity exhaustion. All architectures must prevent both.

## Decision: domain-scoped placement, not one universal host

| Domain | Recommended provider | Use | Explicit exclusions |
| --- | --- | --- | --- |
| CRM-SOFFT operational PostgreSQL | **Dedicated Neon Free project** in eu-central-1 if available | Workspaces, pipelines, task queue metadata, permitted CRM transactional state | Do not mix with CONSTRUCTOR staging or Continuity Memory; no uncontrolled bulk telemetry |
| CRM API / portal frontend | Existing Netlify site or Cloudflare Workers (new account integration only after approval) | Authenticated views and lightweight APIs; backend roles only | No privileged secrets in browser; no promise of 24/7 worker uptime from serverless/free tiers |
| Lightweight public leads/intake cache | Cloudflare Workers + optional D1 | Strictly non-sensitive public records, deduplication, bounded rate limits | D1 is SQLite-compatible, not a drop-in PostgreSQL migration; Free per-database limit 500 MB |
| Evidence / archives / backups | Cloudflare R2 Standard or other independent owner-controlled encrypted object store | WORM-style encrypted snapshots, manifests, restore tests | No raw customer data in public buckets or GitHub; no deletion of old source records before restore proof |
| Canonical governance and controlled execution | Supabase / HANTER federation | AI Passport, Guardian Core, Approval Gateway, Audit Ledger, owner stop; explicitly scoped adapters | Do not mirror permissions implicitly across providers or move the authoritative control plane without migration review |
| Public static sites, docs | GitHub Pages / existing Netlify | Static documents and portals | No private DB, credentials or direct service-role keys |
| Noncritical demos | Render Free web service | Demonstration only | Free Render Postgres expires after 30 days; Free compute sleeps, so cannot be authoritative CRM or always-on NCA |
| Commercial production on Vercel Hobby | **REJECT** | Noncommercial prototypes only | Hobby is personal/noncommercial; do not use it for paid CRM workloads |

## Hard provider budget gates

- Supabase Free: monitor database size every hour; internal 70/80/90/100% thresholds; throttle only dispensable writes. Do not claim that throttle resolves quota or protects against all suspensions.
- Neon Free: official public limits (2026-10-02): 1 GB/project, 100 CU-hours/month/project, 10 branches/project; sleep-to-zero can help bursty workloads. Test actual usage and provider acceptable use before commercial cutover.
- Cloudflare Workers Free: 100,000 requests/day; 10 ms CPU/request; bounded cron quotas. Not suitable for full LLM inference.
- Cloudflare D1 Free: 5 GB total account storage, **500 MB maximum per database**, daily row read/write caps; disable nonessential writes before limits.
- Netlify Free: shared 300 credits/month; quota exhaustion can pause the project. Keep production authorizations out of hosted static UI.
- Render Free: idle sleep, ephemeral disk, 30-day expiration of Free Postgres; avoid for durable customer records.
- R2: separate usage and billing controls are mandatory; a free allowance is not an absolute cost ceiling if overages are enabled.

## Multi-orchestrator integration

**Architect -> HANTER AI Command Center -> federated Orchestrators (including ASTRA) -> professional NCA -> bounded service adapters.**

- Every operation carries tenant/workspace, agent AI Passport, approved Enterprise Skill, intended provider adapter, scope, idempotency key, Guardian Core result, Approval Gateway permit, and Audit Ledger evidence.
- ORION remains collective intelligence/advisory, not independent authority to spend or expand network access.
- Respect Zero Trust, Public/Private Boundary and CRYPTO IMPERIAL Ecosystem Boundary; no cross-provider secret sharing.
- No commercial outreach, customer acceptance, payment confirmation or production NCA promotion inferred from development smoke tests.

## Migration sequence (not executed)

1. **Inventory:** measure CRM-SOFFT actual rows and sizes, Postgres extensions, triggers, RLS functions, JWT/auth assumptions, FK constraints, cron, edge functions, APIs and tenant ownership. Identify the single canonical write authority per table.
2. **Proof-safe archive first:** create encrypted offsite backup for historical Supabase runtime logs and hash-chain evidence; record signed SHA-256 manifest and successfully restore a test sample elsewhere. No destructive cleanup before evidence-based verification.
3. **Provision separate Neon CRM project:** distinct project, EU region, dedicated least-privilege DB roles and endpoint credentials. Never use existing Constructor staging/Continuity DB as CRM production.
4. **Portable schema migration:** diff PostgreSQL versions; replace Supabase-specific `auth.uid()`, `auth.jwt()`, storage/edge assumptions with audited independent auth adapter; enforce tenant RLS on the destination and fail closed.
5. **Read-only shadow:** migrate only explicitly authorized non-sensitive sample data first. Reconcile row counts and keyed SHA-256 checksums; verify application CRUD in isolation (no external outreach).
6. **Controlled cutover:** only with Architect approval, verified independent backup, restore drill, budget guard, owner kill switch, independent QA and documented rollback.
7. **Post-cutover:** observe for a full operating cycle, watch latency, denied requests and 402/429/403 incidents. Archive/compact only verified legacy histories after the new path is stable.
8. **Failover:** default fail-closed on suspension, policy breach, quota exceeded, provider auth errors. Do **not** create replacement accounts to evade provider controls.

## Acceptance checklist

- [ ] Provider rights and commercial-use terms reviewed for each service
- [ ] No monthly billing or auto-recharge introduced
- [ ] Dedicated CRM database separate from other IMPERIAL workloads
- [ ] Tenant isolation and RLS penetration tests pass
- [ ] External encrypted backup and restore drill pass
- [ ] Signed manifests preserve Audit Ledger chain and rollback checkpoints
- [ ] End-to-end CRM job with authorized NCA runs and independent QA passes
- [ ] Cloud requests/load budget recorded, provider alerts active
- [ ] Zero known violations of bundled AI quota relay policies
- [ ] Architect approves production cutover

## Verification boundary

As of 2026-11-04 this ADR is **proposal only**. It does not mean a Neon CRM project, Cloudflare account, archive, synchronization, commercial readiness, or new 24/7 runtime has been deployed. The current Supabase database is still above its reference Free size quota, so the first emergency priority remains evidence-safe export and space reclamation.

## Primary vendor references

- Neon project limits: https://neon.com/blog/neon-free-plan-1-gb-per-project
- Workers limits: https://developers.cloudflare.com/workers/platform/limits/
- D1 Free pricing: https://developers.cloudflare.com/d1/platform/pricing/
- D1 per-database limits: https://developers.cloudflare.com/d1/platform/limits/
- R2 pricing: https://developers.cloudflare.com/r2/pricing/
- Netlify Free: https://www.netlify.com/pricing/
- Render Free limitations: https://render.com/docs/free
- Vercel Hobby restrictions: https://vercel.com/docs/plans/hobby
