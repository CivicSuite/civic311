"""Open311-compatible export helpers for Civic311 v0.1.1."""

from __future__ import annotations

from dataclasses import dataclass

from civic311.request_intake import DISCLAIMER


@dataclass(frozen=True)
class Open311Export:
    service_request_id: str
    service_code: str
    export_fields: tuple[str, ...]
    records_note: str
    disclaimer: str = DISCLAIMER


def build_open311_export(
    *, service_request_id: str, service_code: str, format: str = "json"
) -> Open311Export:
    """Return an Open311-compatible export checklist without writing to another system."""

    fields = (
        "service_request_id",
        "service_code",
        "description",
        "address_string",
        "lat",
        "long",
        "requested_datetime",
        "status",
        "media_url",
    )
    return Open311Export(
        service_request_id=service_request_id.strip() or "unassigned-request",
        service_code=service_code.strip() or "general",
        export_fields=fields,
        records_note=(
            f"Export format '{format}' is a staff-reviewed handoff artifact; it does not write "
            "to an official 311 or work-order system."
        ),
    )
