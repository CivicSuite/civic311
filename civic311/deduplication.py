"""Duplicate-candidate helpers for Civic311 v0.1.0."""

from __future__ import annotations

from dataclasses import dataclass

from civic311.request_intake import DISCLAIMER


@dataclass(frozen=True)
class DuplicateCheck:
    request_id: str
    candidate_count: int
    possible_duplicate: bool
    review_notes: tuple[str, ...]
    disclaimer: str = DISCLAIMER


def check_duplicate_candidates(
    *, request_id: str, category: str, location: str, candidate_count: int
) -> DuplicateCheck:
    """Flag duplicate candidates without merging or closing requests."""

    possible = candidate_count > 0
    notes = (
        f"Search category '{category.strip() or 'unspecified'}' near '{location.strip() or 'unknown location'}'.",
        f"{candidate_count} possible duplicate candidate(s) require staff review.",
        "Civic311 never merges, closes, or suppresses resident requests automatically.",
    )
    return DuplicateCheck(
        request_id=request_id.strip() or "unassigned-request",
        candidate_count=max(candidate_count, 0),
        possible_duplicate=possible,
        review_notes=notes,
    )
