#!/usr/bin/env python3
"""
API Governance Compliance Checker
----------------------------------
Reads an OpenAPI spec + a governance ruleset, checks every endpoint against
every rule, and produces a markdown compliance report. Modeled on the kind
of manual API governance review process used for platforms like Autodesk
Forge/APS: balancing developer access against security & compliance.

Usage:
    python checker.py --spec data/sample_api_spec.json --rules rules.yaml --out output/report.md

If ANTHROPIC_API_KEY is set in the environment, the tool also asks Claude to
write a short executive summary of the findings on top of the deterministic
rule results. Without a key, it still produces the full rule-by-rule report
using local logic only — the AI layer is additive, not required.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime

import yaml

PII_PATTERN = re.compile(r"(email|ssn|password|token|passport|nric)", re.IGNORECASE)
VERSION_PATTERN = re.compile(r"^/v\d+/")


def load_spec(path):
    with open(path) as f:
        return json.load(f)


def load_rules(path):
    with open(path) as f:
        return yaml.safe_load(f)["rules"]


def check_endpoint(path, method, op):
    """Run every deterministic rule against a single (path, method) operation.
    Returns a list of (rule_id, severity, passed, detail)."""
    results = []

    # AUTH-001
    has_auth = bool(op.get("security"))
    results.append(("AUTH-001", "HIGH", has_auth,
                     "No security requirement declared." if not has_auth else "OK"))

    # VER-001
    versioned = bool(VERSION_PATTERN.match(path))
    results.append(("VER-001", "MEDIUM", versioned,
                     f"Path '{path}' is not versioned." if not versioned else "OK"))

    # PII-001 — check query params for suspicious names
    pii_hit = None
    for p in op.get("parameters", []):
        if p.get("in") == "query" and PII_PATTERN.search(p.get("name", "")):
            pii_hit = p["name"]
            break
    results.append(("PII-001", "HIGH", pii_hit is None,
                     f"Query param '{pii_hit}' looks like raw PII." if pii_hit else "OK"))

    # RATE-001
    has_429 = "429" in op.get("responses", {})
    results.append(("RATE-001", "LOW", has_429,
                     "No 429 response documented." if not has_429 else "OK"))

    # DEPRECATE-001 — only flags if summary/description suggests legacy but doesn't say deprecated
    text = f"{op.get('summary', '')} {op.get('description', '')}".lower()
    looks_legacy = "legacy" in text or "old" in text
    says_deprecated = "deprecat" in text
    deprecate_ok = not looks_legacy or says_deprecated
    results.append(("DEPRECATE-001", "MEDIUM", deprecate_ok,
                     "Looks legacy but isn't marked deprecated." if not deprecate_ok else "OK"))

    return results


def run_checks(spec):
    findings = []
    for path, methods in spec.get("paths", {}).items():
        for method, op in methods.items():
            for rule_id, severity, passed, detail in check_endpoint(path, method, op):
                findings.append({
                    "path": path,
                    "method": method.upper(),
                    "rule_id": rule_id,
                    "severity": severity,
                    "passed": passed,
                    "detail": detail,
                })
    return findings


def summarize(findings):
    total = len(findings)
    failed = [f for f in findings if not f["passed"]]
    by_severity = {}
    for f in failed:
        by_severity.setdefault(f["severity"], 0)
        by_severity[f["severity"]] += 1
    return total, failed, by_severity


def claude_executive_summary(failed_findings):
    """Optional: ask Claude for a short exec-ready summary. Falls back to None
    if no API key is configured, so the tool works fully offline."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key or not failed_findings:
        return None
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        findings_text = "\n".join(
            f"- {f['method']} {f['path']}: {f['rule_id']} ({f['severity']}) — {f['detail']}"
            for f in failed_findings
        )
        message = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=400,
            messages=[{
                "role": "user",
                "content": (
                    "You are an API governance reviewer. Given these rule violations, "
                    "write a 3-4 sentence executive summary for a platform leadership "
                    "audience: what's the overall risk posture, and what should be fixed "
                    "first. Be direct, no fluff.\n\n" + findings_text
                ),
            }],
        )
        return message.content[0].text
    except Exception as e:
        return f"(Claude summary unavailable: {e})"


def write_report(findings, out_path, exec_summary=None):
    total, failed, by_severity = summarize(findings)
    lines = []
    lines.append("# API Governance Compliance Report")
    lines.append(f"_Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}_")
    lines.append("")
    lines.append(f"**{len(failed)} of {total} checks failed** across all endpoints.")
    if by_severity:
        sev_line = ", ".join(f"{v} {k}" for k, v in sorted(by_severity.items()))
        lines.append(f"Severity breakdown: {sev_line}")
    lines.append("")

    if exec_summary:
        lines.append("## Executive Summary (Claude)")
        lines.append(exec_summary.strip())
        lines.append("")

    lines.append("## Findings")
    lines.append("")
    lines.append("| Endpoint | Rule | Severity | Status | Detail |")
    lines.append("|---|---|---|---|---|")
    for f in findings:
        status = "PASS" if f["passed"] else "**FAIL**"
        lines.append(
            f"| {f['method']} {f['path']} | {f['rule_id']} | {f['severity']} | {status} | {f['detail']} |"
        )

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write("\n".join(lines))
    return out_path


def main():
    parser = argparse.ArgumentParser(description="API Governance Compliance Checker")
    parser.add_argument("--spec", required=True, help="Path to OpenAPI JSON spec")
    parser.add_argument("--rules", required=True, help="Path to rules.yaml")
    parser.add_argument("--out", default="output/report.md", help="Output markdown path")
    args = parser.parse_args()

    spec = load_spec(args.spec)
    load_rules(args.rules)  # validated / loaded for future rule-driven checks
    findings = run_checks(spec)
    _, failed, _ = summarize(findings)
    exec_summary = claude_executive_summary(failed)
    out_path = write_report(findings, args.out, exec_summary)
    print(f"Report written to {out_path}")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("(Set ANTHROPIC_API_KEY to also get a Claude-written executive summary.)")


if __name__ == "__main__":
    sys.exit(main())
