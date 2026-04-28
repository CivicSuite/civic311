from fastapi.testclient import TestClient

from civic311.deduplication import check_duplicate_candidates
from civic311.main import app
from civic311.open311_export import build_open311_export
from civic311.request_intake import create_service_request_stub
from civic311.routing import plan_department_route
from civic311.triage import suggest_triage


client = TestClient(app)


def test_request_intake_flags_staff_review_boundary() -> None:
    result = create_service_request_stub(
        request_id="sr-001",
        category="pothole",
        description="Large pothole near library entrance",
        location="100 Main St",
    )
    assert result.request_id == "sr-001"
    assert any("urgent" in note for note in result.intake_notes)
    assert "system-of-record updates" in result.disclaimer


def test_triage_suggests_department_without_dispatch() -> None:
    result = suggest_triage(
        category="street",
        description="blocked road hazard",
        location="5th Ave",
    )
    assert result.priority == "urgent-review"
    assert result.suggested_department == "Public Works"
    assert result.staff_review_required is True


def test_duplicate_check_never_merges_automatically() -> None:
    result = check_duplicate_candidates(
        request_id="sr-002",
        category="graffiti",
        location="Park wall",
        candidate_count=2,
    )
    assert result.possible_duplicate is True
    assert "never merges" in result.review_notes[2]


def test_routing_plan_requires_resident_update() -> None:
    result = plan_department_route(category="trash", department="Neighborhood Services")
    assert result.department == "Neighborhood Services"
    assert result.resident_update_required is True
    assert "tracking number" in result.handoff_steps[2]


def test_open311_export_preserves_standard_fields() -> None:
    result = build_open311_export(service_request_id="sr-003", service_code="pothole")
    assert result.service_request_id == "sr-003"
    assert "service_request_id" in result.export_fields
    assert "official 311 or work-order system" in result.records_note


def test_civic311_support_apis_success_shape() -> None:
    intake = client.post(
        "/api/v1/civic311/intake",
        json={
            "request_id": "sr-001",
            "category": "pothole",
            "description": "Large pothole near library entrance",
            "location": "100 Main St",
        },
    )
    triage = client.post(
        "/api/v1/civic311/triage",
        json={"category": "street", "description": "blocked road hazard", "location": "5th Ave"},
    )
    duplicates = client.post(
        "/api/v1/civic311/deduplicate",
        json={"request_id": "sr-002", "category": "graffiti", "location": "Park wall", "candidate_count": 2},
    )
    routing = client.post(
        "/api/v1/civic311/routing",
        json={"category": "trash", "department": "Neighborhood Services"},
    )
    export = client.post(
        "/api/v1/civic311/open311-export",
        json={"service_request_id": "sr-003", "service_code": "pothole"},
    )
    assert intake.status_code == 200
    assert intake.json()["request_id"] == "sr-001"
    assert triage.status_code == 200
    assert triage.json()["suggested_department"] == "Public Works"
    assert duplicates.status_code == 200
    assert duplicates.json()["possible_duplicate"] is True
    assert routing.status_code == 200
    assert routing.json()["resident_update_required"] is True
    assert export.status_code == 200
    assert "service_code" in export.json()["export_fields"]


def test_public_ui_route_is_accessible_and_honest() -> None:
    response = client.get("/civic311")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    text = response.text
    assert '<a class="skip-link" href="#main">Skip to main content</a>' in text
    assert '<main id="main" tabindex="-1">' in text
    assert "v0.1.1 resident service request foundation" in text
    assert "does not create official work orders" in text
    assert "replace the system of record" in text
