# Production Depth: Request Persistence

## Summary

Civic311 now supports optional SQLAlchemy-backed service request and triage review records through `CIVIC311_REQUEST_DB_URL`.

## Shipped

- `ServiceRequestRepository` with schema-aware SQLAlchemy tables.
- Persisted service request records.
- Persisted triage review records.
- Retrieval endpoints:
  - `GET /api/v1/civic311/intake/{request_id}`
  - `GET /api/v1/civic311/triage/{request_id}`
- Actionable `503` guidance when persistence is not configured.
- Regression tests for repository reload, API round trip, missing-record `404`, no-config `503`, and stateless fallback behavior.

## Still Not Shipped

- Official dispatch.
- Work-order creation.
- Emergency response.
- Legal advice.
- Live LLM calls.
- 311 system write-back or system-of-record integrations.
