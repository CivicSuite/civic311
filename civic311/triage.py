"""Resident request triage helpers for Civic311 v0.1.0."""

from __future__ import annotations

from dataclasses import dataclass

from civic311.request_intake import DISCLAIMER


@dataclass(frozen=True)
class TriageSuggestion:
    category: str
    priority: str
    suggested_department: str
    reasons: tuple[str, ...]
    staff_review_required: bool
    disclaimer: str = DISCLAIMER


def suggest_triage(*, category: str, description: str, location: str) -> TriageSuggestion:
    """Suggest a deterministic triage bucket without dispatching work."""

    text = f"{category} {description} {location}".lower()
    if any(term in text for term in ("water main", "sinkhole", "blocked road", "hazard")):
        priority = "urgent-review"
        department = "Public Works"
    elif any(term in text for term in ("graffiti", "trash", "dumping", "pothole")):
        priority = "standard"
        department = "Neighborhood Services"
    else:
        priority = "needs-classification"
        department = "311 Coordinator"

    reasons = (
        f"Matched category '{category.strip() or 'unspecified'}' against deterministic routing hints.",
        f"Location context retained for staff verification: {location.strip() or 'none supplied'}.",
        "Staff must confirm priority, ownership, duplicate status, and dispatch eligibility.",
    )
    return TriageSuggestion(
        category=category.strip() or "general service request",
        priority=priority,
        suggested_department=department,
        reasons=reasons,
        staff_review_required=True,
    )
