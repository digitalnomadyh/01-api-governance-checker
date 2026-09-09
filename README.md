# API Governance Compliance Checker

Reads an OpenAPI spec and a YAML governance ruleset, checks every endpoint
against every rule, and produces a markdown compliance report. Modeled on
the kind of manual API governance review process used for platforms like
Autodesk Forge/APS: balancing developer access against security & compliance.

## Rules checked

| Rule ID | Severity | Description |
|---|---|---|
| AUTH-001 | HIGH | Every endpoint must declare a security requirement (no anonymous access). |
| VER-001 | MEDIUM | Every path must be versioned (starts with `/v1`, `/v2`, etc.). |
| PII-001 | HIGH | No query parameter name may suggest raw PII (email, ssn, password, token). |
| RATE-001 | LOW | Every endpoint should document a rate-limit response (429). |
| DEPRECATE-001 | MEDIUM | Deprecated endpoints must say so in their description. |

Rules are defined in [rules.yaml](rules.yaml) and enforced by the
deterministic checks in [checker.py](checker.py).

## Requirements

- Python 3.8+
- [`PyYAML`](https://pypi.org/project/PyYAML/)
- (Optional) [`anthropic`](https://pypi.org/project/anthropic/) — only needed
  if you want Claude to write an executive summary on top of the report

```bash
pip install pyyaml anthropic
```

## Usage

```bash
python checker.py --spec data/sample_api_spec.json --rules rules.yaml --out output/report.md
```

- `--spec` — path to an OpenAPI JSON spec
- `--rules` — path to the governance ruleset (`rules.yaml`)
- `--out` — path to write the markdown report (default: `output/report.md`)

The tool prints the output path when done:

```
Report written to output/report.md
```

### Optional: Claude executive summary

If `ANTHROPIC_API_KEY` is set in the environment, the report also includes a
short executive summary written by Claude, on top of the deterministic
rule-by-rule results:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
python checker.py --spec data/sample_api_spec.json --rules rules.yaml --out output/report.md
```

Without the key, the tool still produces the full report using local rule
logic only — the AI layer is additive, not required.

## Example

Run the checker against the sample spec:

```bash
python checker.py --spec data/sample_api_spec.json --rules rules.yaml
```

This checks each path/method in [data/sample_api_spec.json](data/sample_api_spec.json)
against all five rules and writes a table of pass/fail results to
`output/report.md`, along with a severity breakdown of any failures.
