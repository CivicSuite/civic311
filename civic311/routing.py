"""Department routing helpers for Civic311 v0.1.1."""

from __future__ import annotations

from dataclasses import dataclass

from civic311.request_intake import DISCLAIMER


@dataclass(frozen=True)
class RoutingPlan:
    category: str
    department: str
    handoff_steps: tuple[str, ...]
    resident_update_required: bool
    disclaimer: str = DISCLAIMER


def plan_department_route(*, category: str, department: str) -> RoutingPlan:
    """Build a staff-owned routing checklist without dispatching work."""

    target = department.strip() or "311 Coordinator"
    steps = (
        f"Confirm {target} owns the request category before assignment.",
        "Check location jurisdiction, service area, and duplicate candidates.",
        "Prepare resident-facing acknowledgment with tracking number and expected next step.",
        "Record any transfer in the city's official 311 or work-order system.",
    )
    return RoutingPlan(
        category=category.strip() or "general service request",
        department=target,
        handoff_steps=steps,
        resident_update_required=True,
    )
