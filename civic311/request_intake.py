"""Resident service request intake helpers for Civic311 v0.1.1."""

from __future__ import annotations

from dataclasses import dataclass


DISCLAIMER = (
    "Civic311 supports resident service request intake and routing, but staff "
    "remain responsible for field verification, prioritization, dispatch, public "
    "communications, and official system-of-record updates."
)


@dataclass(frozen=True)
class ServiceRequestIntake:
    request_id: str
    category: str
    description: str
    location: str
    intake_notes: tuple[str, ...]
    disclaimer: str = DISCLAIMER


def create_service_request_stub(
    *, request_id: str, category: str, description: str, location: str
) -> ServiceRequestIntake:
    """Return a deterministic service-request intake stub for staff review."""

    notes = (
        "Confirm category, location, contact preference, and whether the issue is urgent.",
        "Attach resident-provided photos, source message, parcel or address context, and timestamp.",
        "Route through department triage before dispatch or system-of-record update.",
    )
    return ServiceRequestIntake(
        request_id=request_id.strip() or "unassigned-request",
        category=category.strip() or "general service request",
        description=description.strip() or "No description supplied.",
        location=location.strip() or "Location pending staff review",
        intake_notes=notes,
    )
