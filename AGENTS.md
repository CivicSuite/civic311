# Civic311 Agent Board

## Source of Truth

- Upstream suite spec: `CivicSuite/civicsuite/docs/CivicSuiteUnifiedSpec.md`, especially the Civic311 catalog entry and suite-wide non-negotiables.
- Civic311 supports resident service request intake, deterministic triage, duplicate-candidate review, department routing, and Open311-compatible export checklists.
- Staff own every decision.

## Hard Boundaries

- Civic311 never dispatches crews, creates official work orders, handles emergencies, provides legal advice, writes back to 311/work-order systems, or updates a 311 system of record.
- Civic311 v0.1.1 must not call live LLMs or live 311/work-order systems.
- Triage, duplicate-candidate review, routing, and exports must be marked staff-review-required where applicable.
- Civic311 depends on CivicCore; CivicCore must never depend on Civic311.
- Civic311 may reference CivicAccess and CivicCode concepts only through released APIs or deterministic sample data in v0.1.1.

## Verification

Run `bash scripts/verify-release.sh` before every push or release.
