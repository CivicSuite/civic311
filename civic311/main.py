"""FastAPI runtime foundation for Civic311."""

import os

from civiccore import __version__ as CIVICCORE_VERSION
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from civic311 import __version__
from civic311.deduplication import check_duplicate_candidates
from civic311.open311_export import build_open311_export
from civic311.persistence import ServiceRequestRepository, StoredTriageReview
from civic311.public_ui import render_public_lookup_page
from civic311.request_intake import create_service_request_stub
from civic311.routing import plan_department_route
from civic311.triage import suggest_triage


app = FastAPI(
    title="Civic311",
    version=__version__,
    description="Resident service request intake, triage, deduplication, routing, and Open311-compatible export support for CivicSuite.",
)

_request_repository: ServiceRequestRepository | None = None
_request_db_url: str | None = None


class IntakeRequest(BaseModel):
    request_id: str
    category: str
    description: str
    location: str


class TriageRequest(BaseModel):
    request_id: str = "unassigned-request"
    category: str
    description: str
    location: str


class DeduplicationRequest(BaseModel):
    request_id: str
    category: str
    location: str
    candidate_count: int = 0


class RoutingRequest(BaseModel):
    category: str
    department: str


class Open311ExportRequest(BaseModel):
    service_request_id: str
    service_code: str
    format: str = "json"


@app.get("/")
def root() -> dict[str, str]:
    """Return current product state without overstating unshipped behavior."""

    return {
        "name": "Civic311",
        "version": __version__,
        "status": "resident service request foundation plus request persistence",
        "message": (
            "Civic311 package, API foundation, sample request intake, deterministic triage, "
            "duplicate-candidate review, department routing checklist, optional database-backed service request "
            "and triage review records, Open311-compatible export helper, and public UI foundation are online; "
            "official dispatch, work-order creation, emergency response, legal advice, live LLM calls, and 311 "
            "system-of-record integrations are not implemented yet."
        ),
        "next_step": "Post-v0.1.1 roadmap: configured service catalog, CivicAccess/CivicCode handoffs, and work-order integrations",
    }


@app.get("/health")
def health() -> dict[str, str]:
    """Return dependency/version health for deployment smoke checks."""

    return {
        "status": "ok",
        "service": "civic311",
        "version": __version__,
        "civiccore_version": CIVICCORE_VERSION,
    }


@app.get("/civic311", response_class=HTMLResponse)
def public_civic311_page() -> str:
    """Return the public sample 311 support UI."""

    return render_public_lookup_page()


@app.post("/api/v1/civic311/intake")
def service_request_intake(request: IntakeRequest) -> dict[str, object]:
    result = _create_service_request(
        request_id=request.request_id,
        category=request.category,
        description=request.description,
        location=request.location,
    )
    return result.__dict__


@app.get("/api/v1/civic311/intake/{request_id}")
def get_service_request(request_id: str) -> dict[str, object]:
    if _request_database_url() is None:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "Civic311 request persistence is not configured.",
                "fix": "Set CIVIC311_REQUEST_DB_URL to retrieve persisted service request records.",
            },
        )
    stored = _get_request_repository().get_request(request_id)
    if stored is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Service request record not found.",
                "fix": "Use a request_id returned by POST /api/v1/civic311/intake.",
            },
        )
    return stored.__dict__


@app.post("/api/v1/civic311/triage")
def triage(request: TriageRequest) -> dict[str, object]:
    if _request_database_url() is not None:
        stored = _get_request_repository().create_triage_review(
            request_id=request.request_id,
            category=request.category,
            description=request.description,
            location=request.location,
        )
        return _stored_triage_response(stored)

    return suggest_triage(
        category=request.category,
        description=request.description,
        location=request.location,
    ).__dict__


@app.get("/api/v1/civic311/triage/{request_id}")
def get_triage_review(request_id: str) -> dict[str, object]:
    if _request_database_url() is None:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "Civic311 request persistence is not configured.",
                "fix": "Set CIVIC311_REQUEST_DB_URL to retrieve persisted triage review records.",
            },
        )
    stored = _get_request_repository().get_triage_review(request_id)
    if stored is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Triage review record not found.",
                "fix": "Use a request_id returned by POST /api/v1/civic311/triage.",
            },
        )
    return _stored_triage_response(stored)


@app.post("/api/v1/civic311/deduplicate")
def deduplicate(request: DeduplicationRequest) -> dict[str, object]:
    return check_duplicate_candidates(
        request_id=request.request_id,
        category=request.category,
        location=request.location,
        candidate_count=request.candidate_count,
    ).__dict__


@app.post("/api/v1/civic311/routing")
def routing(request: RoutingRequest) -> dict[str, object]:
    return plan_department_route(
        category=request.category,
        department=request.department,
    ).__dict__


@app.post("/api/v1/civic311/open311-export")
def open311_export(request: Open311ExportRequest) -> dict[str, object]:
    return build_open311_export(
        service_request_id=request.service_request_id,
        service_code=request.service_code,
        format=request.format,
    ).__dict__


def _request_database_url() -> str | None:
    return os.environ.get("CIVIC311_REQUEST_DB_URL")


def _get_request_repository() -> ServiceRequestRepository:
    global _request_db_url, _request_repository
    db_url = _request_database_url()
    if db_url is None:
        raise RuntimeError("CIVIC311_REQUEST_DB_URL is not configured.")
    if _request_repository is None or db_url != _request_db_url:
        _dispose_request_repository()
        _request_db_url = db_url
        _request_repository = ServiceRequestRepository(db_url=db_url)
    return _request_repository


def _dispose_request_repository() -> None:
    global _request_repository
    if _request_repository is not None:
        _request_repository.engine.dispose()
        _request_repository = None


def _create_service_request(*, request_id: str, category: str, description: str, location: str):
    if _request_database_url() is None:
        return create_service_request_stub(
            request_id=request_id,
            category=category,
            description=description,
            location=location,
        )
    return _get_request_repository().create_request(
        request_id=request_id,
        category=category,
        description=description,
        location=location,
    )


def _stored_triage_response(stored: StoredTriageReview) -> dict[str, object]:
    return {
        "request_id": stored.request_id,
        "category": stored.category,
        "priority": stored.priority,
        "suggested_department": stored.suggested_department,
        "reasons": list(stored.reasons),
        "staff_review_required": stored.staff_review_required,
        "disclaimer": stored.disclaimer,
        "created_at": stored.created_at.isoformat(),
    }
