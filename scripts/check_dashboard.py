#!/usr/bin/env python3
"""Dependency-free public dashboard safety and completeness checks."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
HTML = SITE / "index.html"
CSS = SITE / "assets/dashboard.css"
JS = SITE / "assets/dashboard.js"
FEED = SITE / "data/runtime-status.json"

class AssetParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.csp = []
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "script":
            assert "src" in values, "Inline script forbidden"
            self.refs.append(values["src"])
        if tag == "link" and values.get("rel") == "stylesheet":
            self.refs.append(values["href"])
        if tag == "meta" and values.get("http-equiv") == "Content-Security-Policy":
            self.csp.append(values.get("content",""))

def main():
    for path in (HTML, CSS, JS, FEED):
        assert path.is_file() and path.stat().st_size, f"Missing/empty: {path}"
    page = HTML.read_text(encoding="utf8")
    script = JS.read_text(encoding="utf8")
    parser = AssetParser()
    parser.feed(page)
    assert parser.csp and "connect-src 'self' https://api.github.com" in parser.csp[0]
    assert "script-src 'self'" in parser.csp[0]
    for ref in parser.refs:
        assert not ref.startswith(("https:", "http:", "/")), "Asset must be relative and first party"
        assert (SITE / ref).is_file(), f"Broken asset reference: {ref}"
    assert "github.com/oromaskevic23-cmd/IMPERIAL-CRM-Autopilot" in page
    assert "api.github.com" in script
    assert "MAX_RUNTIME_AGE_MS" in script and "payment_verification" in script
    for identifier in ("metric-workers","metric-deliveries","metric-payments","metric-revenue","team-members","github-state","repo-ci","runtime-message"):
        assert f'id="{identifier}"' in page, f"Missing dashboard identifier: {identifier}"
    assert not re.search(r'(?i)(api[_-]?key|secret|private[_-]?key)\s*[:=]\s*["\'][A-Za-z0-9_-]{16,}', script), "Possible credential"
    status = json.loads(FEED.read_text(encoding="utf8"))
    assert status["schema_version"] == 1
    if status["source"] == "unconnected":
        assert status["observed_at"] is None
        assert status["payment_evidence_url"] is None
        assert status["evidence_links"] == []
        assert all(value is None for value in status["metrics"].values()), "Never fake unconnected business metrics"
    print("PASS: dashboard assets, link paths, CSP, source and unconnected-data contract")

if __name__ == "__main__":
    main()
