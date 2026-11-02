"use strict";
/* Public read-only telemetry. No credentials, private leads, or control actions belong here. */
(() => {
  const REPO = "oromaskevic23-cmd/IMPERIAL-CRM-Autopilot";
  const API = "https://api.github.com/repos/" + REPO;
  const POLL_MS = 5 * 60 * 1000;
  const MAX_RUNTIME_AGE_MS = 30 * 60 * 1000;
  const el = id => document.getElementById(id);
  const put = (id, value) => { const node = el(id); if (node) node.textContent = String(value); };
  const num = value => Number.isSafeInteger(value) && value >= 0 ? value.toLocaleString("en-US") : "—";
  const money = (value, currency) => typeof value === "number" && Number.isFinite(value) && value >= 0 && ["USD","EUR","GBP"].includes(currency)
    ? new Intl.NumberFormat("en-US", { style: "currency", currency, maximumFractionDigits: 2 }).format(value) : "—";
  const readableTime = date => {
    const t = new Date(date);
    return Number.isFinite(t.getTime()) ? t.toLocaleString("en-GB", { dateStyle: "medium", timeStyle: "short" }) : "Unknown";
  };
  const squads = {
    freelance: {
      orchestrator: "Freelance Delivery Orchestrator",
      agents: [
        ["Opportunity Scout", "Frankfurt", "Permitted lead discovery"],
        ["Solution Architect", "Warsaw", "Scope, estimate, acceptance"],
        ["Implementation Agent", "Tokyo", "Sandboxed engineering"],
        ["Independent QA", "London", "Evidence-based validation"],
        ["Client Delivery Agent", "New York", "Approved handover"]
      ]
    },
    brokerage: {
      orchestrator: "Brokerage Operations Orchestrator",
      agents: [
        ["Market Scout", "New York", "Public market opportunities"],
        ["Asset Analyst", "Frankfurt", "Comparable evidence"],
        ["Due Diligence", "London", "Ownership and risk review"],
        ["Deal Coordinator", "Dubai", "Human-approved outreach"],
        ["Independent QA", "Singapore", "Document cross-check"]
      ]
    },
    "real-estate": {
      orchestrator: "Real Estate Operations Orchestrator",
      agents: [
        ["Listing Researcher", "Warsaw", "Permitted listing intake"],
        ["Local Market Analyst", "Frankfurt", "Neighborhood comparables"],
        ["Document Analyst", "Dubai", "Legal review preparation"],
        ["Transaction Coordinator", "New York", "Milestones and parties"],
        ["Independent QA", "London", "Evidence and discrepancy checks"]
      ]
    }
  };
  function showSquad(mode) {
    const team = squads[mode];
    if (!team) return;
    put("team-orchestrator", team.orchestrator);
    document.querySelectorAll("[data-mode]").forEach(button => button.setAttribute("aria-pressed", String(button.dataset.mode === mode)));
    const container = el("team-members");
    container.replaceChildren();
    team.agents.forEach(([role, city, description], index) => {
      const card = document.createElement("div"); card.className = "agent";
      const number = document.createElement("span"); number.className = "agent-number"; number.textContent = "NCA · " + String(index + 1).padStart(2,"0");
      const name = document.createElement("strong"); name.textContent = role;
      const location = document.createElement("span"); location.className = "agent-city"; location.textContent = "◈ " + city;
      const purpose = document.createElement("small"); purpose.textContent = description;
      card.append(number, name, location, purpose); container.append(card);
    });
  }
  document.querySelectorAll("[data-mode]").forEach(button => button.addEventListener("click", () => showSquad(button.dataset.mode)));
  showSquad("freelance");

  async function getJson(url, signal) {
    const response = await fetch(url, {
      signal, cache: "no-store",
      headers: { "Accept": "application/vnd.github+json" }
    });
    if (!response.ok) throw new Error("HTTP " + response.status);
    return response.json();
  }
  async function refreshGithub() {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 12000);
    try {
      const results = await Promise.allSettled([
        getJson(API, controller.signal),
        getJson(API + "/commits?per_page=1", controller.signal),
        getJson(API + "/actions/runs?per_page=1", controller.signal)
      ]);
      const repository = results[0];
      if (repository.status !== "fulfilled" || !repository.value || repository.value.full_name !== REPO) {
        throw new Error(repository.status === "rejected" ? repository.reason.message : "Repository response invalid");
      }
      put("repo-stars", num(repository.value.stargazers_count));
      put("repo-forks", num(repository.value.forks_count));
      put("repo-open", num(repository.value.open_issues_count));
      put("repo-commit", results[1].status === "fulfilled" && Array.isArray(results[1].value) && results[1].value[0]?.sha
        ? results[1].value[0].sha.slice(0,7) : "Unavailable");
      const runs = results[2].status === "fulfilled" ? results[2].value?.workflow_runs : null;
      if (Array.isArray(runs) && runs.length) {
        const run = runs[0];
        put("repo-ci", run.status === "completed" ? (run.conclusion || "unknown").toUpperCase() : (run.status || "unknown").toUpperCase());
      } else put("repo-ci", "No run data");
      put("github-state", "GitHub live");
      put("github-badge", "LIVE API");
      el("github-signal").className = "signal ok";
    } catch (error) {
      put("github-state", "GitHub unavailable");
      put("github-badge", "UNAVAILABLE");
      put("repo-ci", "Unavailable");
      el("github-signal").className = "signal failed";
      console.warn("Public GitHub telemetry failed:", error.message);
    } finally { clearTimeout(timeout); }
  }

  const fields = [
    ["metric-workers", "metric-workers-note", "active_nca_workers"],
    ["metric-deliveries", "metric-deliveries-note", "verified_deliveries"],
    ["metric-payments", "metric-payments-note", "confirmed_payments"]
  ];
  function clearRuntime(reason) {
    fields.forEach(([target, note]) => { put(target, "—"); put(note, "Not connected"); });
    put("metric-revenue", "—");
    put("metric-revenue-note", "No payment evidence");
    put("runtime-freshness", "Runtime feed not connected");
    put("runtime-message", reason || "No verified server-side NCA or payment feed has been connected.");
  }
  async function refreshRuntime() {
    try {
      const snapshot = await getJson("data/runtime-status.json?t=" + Date.now());
      const when = new Date(snapshot.observed_at);
      const isFresh = Number.isFinite(when.getTime()) && (Date.now() - when.getTime() >= 0) && (Date.now() - when.getTime() <= MAX_RUNTIME_AGE_MS);
      if (snapshot.schema_version !== 1 || snapshot.source !== "server-readonly-projection" || !isFresh) {
        clearRuntime(snapshot.source === "unconnected"
          ? "The NCA, CRM and payments server feeds are not connected. GitHub telemetry above is independently live."
          : "Runtime data is missing, invalid or stale; the dashboard will not present it as current.");
        return;
      }
      if (!snapshot.metrics || !Array.isArray(snapshot.evidence_links) || snapshot.evidence_links.length === 0) {
        clearRuntime("Incomplete runtime projection: no metrics or audit evidence.");
        return;
      }
      fields.forEach(([target,note,key]) => {
        put(target, num(snapshot.metrics[key]));
        put(note, "Server reported · " + readableTime(snapshot.observed_at));
      });
      const verifiedMoney = snapshot.payment_verification === "provider-confirmed"
        && typeof snapshot.payment_evidence_url === "string"
        && snapshot.payment_evidence_url.startsWith("https://");
      put("metric-revenue", verifiedMoney ? money(snapshot.metrics.confirmed_revenue, snapshot.currency) : "—");
      put("metric-revenue-note", verifiedMoney ? "Provider-backed server report" : "No provider payment proof");
      put("runtime-freshness", "Server report · " + readableTime(snapshot.observed_at));
      put("runtime-message", "Read-only server snapshot. Counts are server-reported, not independently authenticated by GitHub Pages. Review the linked evidence in the source system.");
    } catch (error) {
      clearRuntime("Runtime feed unavailable. No production operations or payment confirmations can be inferred.");
      console.warn("Runtime feed error:", error.message);
    }
  }
  let busy = false;
  async function refresh() {
    if (busy) return;
    busy = true; el("refresh").disabled = true;
    try {
      await Promise.all([refreshGithub(), refreshRuntime()]);
      put("last-refresh", "Checked " + readableTime(new Date().toISOString()));
    } finally { busy = false; el("refresh").disabled = false; }
  }
  el("refresh").addEventListener("click", refresh);
  refresh();
  setInterval(() => { if (!document.hidden) refresh(); }, POLL_MS);
  document.addEventListener("visibilitychange", () => { if (!document.hidden) refresh(); });
})();
