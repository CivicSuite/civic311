# Civic311

Civic311 is the CivicSuite module for resident service request intake, deterministic triage, duplicate-candidate review, department routing, and Open311-compatible export support.

Current state: **v0.1.0 resident service request foundation release**. This repo ships a FastAPI package, health/root endpoints, documentation gates, deterministic sample request intake, triage suggestions, duplicate-candidate checks, routing checklists, Open311-compatible export helper, and accessible public sample UI at `/civic311`. It does **not** ship official dispatch, work-order creation, emergency response, legal advice, live LLM calls, 311 system write-back, or 311 system-of-record integrations.

## What Civic311 Does

- Create sample resident service request intake stubs.
- Suggest deterministic triage buckets for staff review.
- Flag possible duplicates without merging requests.
- Build department routing and resident-update checklists.
- Produce Open311-compatible export checklists.
- Demonstrate a public service-request UI at `/civic311`.

## What Civic311 Does Not Do

- It does not dispatch crews or create official work orders.
- It does not handle emergencies.
- It does not provide legal advice.
- It does not call live LLMs in v0.1.0.
- It does not write back to 311 or work-order systems.
- It does not replace a 311 system of record.

## API Surface

- `GET /` returns the shipped/planned boundary.
- `GET /health` returns package and CivicCore versions.
- `GET /civic311` returns the accessible public sample UI.
- `POST /api/v1/civic311/intake` returns a sample request intake stub.
- `POST /api/v1/civic311/triage` returns deterministic triage suggestions.
- `POST /api/v1/civic311/deduplicate` returns duplicate-candidate review notes.
- `POST /api/v1/civic311/routing` returns department-routing checklists.
- `POST /api/v1/civic311/open311-export` returns an Open311-compatible export checklist.

## Local Development

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
bash scripts/verify-release.sh
```

## License

Code is Apache License 2.0. Documentation is CC BY 4.0.
