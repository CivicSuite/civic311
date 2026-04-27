# Changelog

All notable changes to Civic311 will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.1.0] - 2026-04-27

### Added

- FastAPI package/runtime foundation pinned to `civiccore==0.2.0`.
- Resident service request intake helper using deterministic sample data.
- Triage suggestion helper with staff-verification boundary.
- Duplicate-candidate helper that never merges or closes requests automatically.
- Department routing helper with resident-update checklist.
- Open311-compatible export checklist.
- Accessible public sample UI at `/civic311` with browser QA coverage.
- Release gate: tests, docs, placeholder import guard, Ruff, and build artifact checks.

### Not Shipped

- Official dispatch, work-order creation, emergency response, legal advice, live LLM calls, 311 system write-back, and 311 system-of-record integrations.
