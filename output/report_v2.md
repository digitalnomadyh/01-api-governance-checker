# API Governance Compliance Report
_Generated 2026-09-09 12:23_

**6 of 20 checks failed** across all endpoints.
Severity breakdown: 3 HIGH, 1 LOW, 2 MEDIUM

## Findings

| Endpoint | Rule | Severity | Status | Detail |
|---|---|---|---|---|
| GET /v2/notifications | AUTH-001 | HIGH | PASS | OK |
| GET /v2/notifications | VER-001 | MEDIUM | PASS | OK |
| GET /v2/notifications | PII-001 | HIGH | PASS | OK |
| GET /v2/notifications | RATE-001 | LOW | PASS | OK |
| GET /v2/notifications | DEPRECATE-001 | MEDIUM | PASS | OK |
| POST /v2/notifications/{id}/read | AUTH-001 | HIGH | PASS | OK |
| POST /v2/notifications/{id}/read | VER-001 | MEDIUM | PASS | OK |
| POST /v2/notifications/{id}/read | PII-001 | HIGH | PASS | OK |
| POST /v2/notifications/{id}/read | RATE-001 | LOW | PASS | OK |
| POST /v2/notifications/{id}/read | DEPRECATE-001 | MEDIUM | PASS | OK |
| POST /v1/webhooks/register | AUTH-001 | HIGH | **FAIL** | No security requirement declared. |
| POST /v1/webhooks/register | VER-001 | MEDIUM | PASS | OK |
| POST /v1/webhooks/register | PII-001 | HIGH | **FAIL** | Query param 'secret_token' looks like raw PII. |
| POST /v1/webhooks/register | RATE-001 | LOW | **FAIL** | No 429 response documented. |
| POST /v1/webhooks/register | DEPRECATE-001 | MEDIUM | **FAIL** | Looks legacy but isn't marked deprecated. |
| GET /admin/debug/session | AUTH-001 | HIGH | PASS | OK |
| GET /admin/debug/session | VER-001 | MEDIUM | **FAIL** | Path '/admin/debug/session' is not versioned. |
| GET /admin/debug/session | PII-001 | HIGH | **FAIL** | Query param 'user_password' looks like raw PII. |
| GET /admin/debug/session | RATE-001 | LOW | PASS | OK |
| GET /admin/debug/session | DEPRECATE-001 | MEDIUM | PASS | OK |