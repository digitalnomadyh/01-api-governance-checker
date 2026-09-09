# API Governance Compliance Report
_Generated 2026-09-09 12:19_

**7 of 20 checks failed** across all endpoints.
Severity breakdown: 2 HIGH, 3 LOW, 2 MEDIUM

## Findings

| Endpoint | Rule | Severity | Status | Detail |
|---|---|---|---|---|
| GET /v1/projects/{id}/entitlements | AUTH-001 | HIGH | PASS | OK |
| GET /v1/projects/{id}/entitlements | VER-001 | MEDIUM | PASS | OK |
| GET /v1/projects/{id}/entitlements | PII-001 | HIGH | PASS | OK |
| GET /v1/projects/{id}/entitlements | RATE-001 | LOW | PASS | OK |
| GET /v1/projects/{id}/entitlements | DEPRECATE-001 | MEDIUM | PASS | OK |
| GET /v1/users/lookup | AUTH-001 | HIGH | PASS | OK |
| GET /v1/users/lookup | VER-001 | MEDIUM | PASS | OK |
| GET /v1/users/lookup | PII-001 | HIGH | **FAIL** | Query param 'email' looks like raw PII. |
| GET /v1/users/lookup | RATE-001 | LOW | **FAIL** | No 429 response documented. |
| GET /v1/users/lookup | DEPRECATE-001 | MEDIUM | PASS | OK |
| GET /legacy/reports | AUTH-001 | HIGH | **FAIL** | No security requirement declared. |
| GET /legacy/reports | VER-001 | MEDIUM | **FAIL** | Path '/legacy/reports' is not versioned. |
| GET /legacy/reports | PII-001 | HIGH | PASS | OK |
| GET /legacy/reports | RATE-001 | LOW | **FAIL** | No 429 response documented. |
| GET /legacy/reports | DEPRECATE-001 | MEDIUM | **FAIL** | Looks legacy but isn't marked deprecated. |
| POST /v1/ai/feature-access | AUTH-001 | HIGH | PASS | OK |
| POST /v1/ai/feature-access | VER-001 | MEDIUM | PASS | OK |
| POST /v1/ai/feature-access | PII-001 | HIGH | PASS | OK |
| POST /v1/ai/feature-access | RATE-001 | LOW | **FAIL** | No 429 response documented. |
| POST /v1/ai/feature-access | DEPRECATE-001 | MEDIUM | PASS | OK |