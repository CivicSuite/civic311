Civic311
========

Civic311 is the CivicSuite module for resident service request intake, deterministic triage, duplicate-candidate review, department routing, and Open311-compatible export support.

Current state: v0.1.1 resident service request foundation plus request persistence release, aligned to civiccore==0.3.0. This repo ships a FastAPI package, health/root endpoints, documentation gates, deterministic sample request intake, triage suggestions, optional database-backed service request and triage review records, duplicate-candidate checks, routing checklists, Open311-compatible export helper, and accessible public sample UI at /civic311.

It does not ship official dispatch, work-order creation, emergency response, legal advice, live LLM calls, 311 system write-back, or 311 system-of-record integrations.

What Civic311 does:
- Create sample resident service request intake stubs.
- Suggest deterministic triage buckets for staff review.
- Flag possible duplicates without merging requests.
- Build department routing and resident-update checklists.
- Produce Open311-compatible export checklists.
- Demonstrate a public service-request UI at /civic311.

API surface:
- GET /
- GET /health
- GET /civic311
- POST /api/v1/civic311/intake
- GET /api/v1/civic311/intake/{request_id}
- POST /api/v1/civic311/triage
- GET /api/v1/civic311/triage/{request_id}
- POST /api/v1/civic311/deduplicate
- POST /api/v1/civic311/routing
- POST /api/v1/civic311/open311-export

Optional persistence: set CIVIC311_REQUEST_DB_URL to enable SQLAlchemy-backed service request and triage review records. Without it, Civic311 remains deterministic and stateless.

License: Apache License 2.0 for code; CC BY 4.0 for documentation.
