# CRM-SOFFT — Sprint 003: IMPERIAL Core NCA Release Authority Gate

**Date:** 2026-11-03  
**Author / Final Architectural Decision Authority:** Alexander Nikolaevich Romaskevich (RomaskevicH), Founder • Owner • CEO.  
**Budget:** FREE_ONLY.  
**Status:** executable local readiness classifier + negative tests in CI. **NOT an authenticated production authority service.**

## Why this matters to IMPERIAL Core

This work is about IMPERIAL Core itself: getting one professionally trained, scoped Nano Core Agent reliably into a real, correctly governed business workflow. Counting registered agent records, open research leads, or simulated quotes as deployed staff, customers, or revenue is unacceptable.

The canonical architecture remains **Architect → HANTER (AI Command Center) → multiple federated domain orchestrators → NCA execution**. Preserve ORION, VELION (MAX is a mode), LEGION, AI Passport, Enterprise Skills, Guardian Core, Approval Gateway, Audit Ledger, ProofGraph, IntentLock, Owner Kill Switch, Zero Trust, Public/Private Boundary and CRYPTO IMPERIAL Ecosystem Boundary. No omnipotent global orchestrator.

## Code delivered

- [crm_control/release_gate.py](../crm_control/release_gate.py) — strict JSON-like schema for *aggregated* CRM posture; rejects unexpected PII, malformed status labels, inconsistent agent totals, stale timestamps, forged status types and missing approval booleans.
- [tests/test_crm_release_gate.py](../tests/test_crm_release_gate.py) — 26 negative/positive contract tests.
- [crm_control/__main__.py](../crm_control/__main__.py) — one no-network, explicitly **synthetic** operating-posture demonstration. Prints `synthetic_fixture_not_real_crm: true`; cannot dispatch or book money.
- [GitHub Actions verification](https://github.com/oromaskevic23-cmd/IMPERIAL-CRM-Autopilot/actions/runs/41685910346) — **26/26 PASS** on Python 3.11 and **26/26 PASS** on Python 3.12.

## Business gates that are never inferred from self-reported counts

| External action | Readiness-gate result | Required independent authority |
| --- | --- | --- |
| Start actual NCA worker | **DENY** | Registered Owner signing trust, signed revocable AI Passport, Guardian Core, Approval Gateway, managed worker and verified STOP |
| Contact or solicit a real lead | **DENY** | Documented source rights, customer mandate and protected Approval Gateway |
| Mark payment confirmed | **DENY** | Signed provider settlement, account/invoice reconciliation, independent ledger evidence |
| Publish private customer data | **DENY** | Public/Private Boundary and explicit consent; no automatic personal-data export |
| Transfer root Owner/Architect authority | **DENY** | Never permitted through NCA automation; separate out-of-band governance procedure |

An input with every `verified_gates` field set to `true` **still does not grant production access**, because supplied flags are not an independently trusted signed attestation. The module intentionally returns `production_authorized:false`, `hanter_production_connection_verified:false` and `public_publishable:false`. A fingerprint of aggregate content is an integrity hint, not a proof of origin.

## Existing Supabase facts — private-only provenance

A separately performed **read-only** check of the existing `crm_sofft` schema on 3 November 2026 observed 11 workspace records all in `CONFIGURING`, 21 agent records all in `REGISTERED_NOT_AUTHORIZED` with `guardian_state=NOT_VERIFIED`, 14 lead records (3 qualification needed, 1 waiting after outreach, 10 research-only), 26 task records (24 draft, 2 blocked), and zero rows in the checked `payment_records` and `revenue_ledger` tables.

**This is not proof of zero money enterprise-wide or proof of active workers.** The associated aggregate snapshot is stored **only in the private IMPERIAL Core governance repository**, not in this public repo. It contains no customer identities, account details, passports or secrets. Its database origin is operator-recorded but **not cryptographically attested**.

## Real governance blockers — not hidden

- Actual Owner Ed25519 enrollment, AI Passport issuer/revocation, managed worker and independent professional examination are not yet connected to the CRM production route.
- Real `crm_sofft` database contains production-shaped records, but the new application bridge still has no privately configured, tenant-scoped, least-privilege connection. Its existing PostgreSQL 17 verification used an ephemeral isolated test database.
- Separate database review observed RLS-disabled tables in `imperial_control`/`imperial_crm`; ordinary `anon`/`authenticated` table privileges were denied on the reviewed operations. Some SECURITY DEFINER functions have default `EXECUTE` grants but live in schemas without `USAGE` for those ordinary roles. **Do not claim an exploitable public endpoint** without verifying reachability and dependent functions. Restrict privileges through a reviewed migration after dependency testing, not indiscriminately.
- Proof of a signed payment, actual qualified client acceptance, professionally verified NCA output, or authorized public publishing remains absent.

## Next production sprint: one strictly authorized success

1. **One reporting identity:** create a role with read-only, least-privileged access to an approved *tenant-aware* aggregate projection; independently prove it cannot read another tenant or write. Do not grant `service_role` to client apps or disable RLS.
2. **One Owner-approved candidate NCA:** complete real protected Owner key enrollment, AI Passport, skill assessment, verified Guardian and Approval Gateway, plus measured remote stop on a managed worker.
3. **One genuine lead:** review one of the qualification-needed records inside the protected CRM with client consent and source evidence. HANTER routes only that permitted case to the appropriate federated orchestrator. No automated outreach until mandate verification.
4. **One accepted deliverable:** independent LEGION examiner reviews the actual artifact, reproduces results and signs evidence into Audit Ledger.
5. **One settlement:** recognize `PAYMENT_CONFIRMED` only after external provider reconciliation, verified client/beneficiary and invoice linkage. Until then, revenue remains **unverified**, not an invented positive number.

## Reproduction

From repository root, without API keys or installing dependencies:

```bash
python3 -m unittest discover -s tests -p 'test_crm_release_gate.py' -v
python3 -m crm_control
```

The second command uses invented test aggregates **solely to exercise the gate**. Do not present its output as current operational telemetry. To display real private status, first obtain an authorized, privacy-safe, attested aggregate from a separately protected server-side pipeline.

**Build software. Verify everything.**
