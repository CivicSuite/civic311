# Contributing

Thank you for helping Civic311 become useful municipal software.

## Development Loop

1. Read `AGENTS.md`, `docs/RECONCILIATION.md`, and `docs/MILESTONES.md`.
2. Create tests before implementation for each milestone.
3. Keep docs and tests in the same PR as code changes.
4. Run `bash scripts/verify-release.sh` before push.

## Boundaries

- Civic311 gives request-support drafts, not official dispatch, emergency response, work-order creation, legal advice, 311 system write-back, or system-of-record updates.
- Do not present generated triage suggestions, duplicate flags, routing plans, or Open311 exports as dispatch-ready without staff review.
- Do not import CivicCore placeholder packages.
- Do not claim planned behavior is shipped.
