from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from civic311.main import app, _dispose_request_repository
from civic311.persistence import ServiceRequestRepository


client = TestClient(app)


def test_repository_persists_request_and_triage_review(tmp_path: Path) -> None:
    db_path = tmp_path / "civic311.db"
    db_url = f"sqlite+pysqlite:///{db_path.as_posix()}"

    repository = ServiceRequestRepository(db_url=db_url)
    request = repository.create_request(
        request_id="sr-001",
        category="street",
        description="blocked road hazard",
        location="5th Ave",
    )
    triage = repository.create_triage_review(
        request_id="sr-001",
        category="street",
        description="blocked road hazard",
        location="5th Ave",
    )
    repository.engine.dispose()

    reloaded = ServiceRequestRepository(db_url=db_url)
    stored_request = reloaded.get_request(request.request_id)
    stored_triage = reloaded.get_triage_review(triage.request_id)
    reloaded.engine.dispose()

    assert stored_request is not None
    assert stored_request.location == "5th Ave"
    assert stored_triage is not None
    assert stored_triage.priority == "urgent-review"
    assert stored_triage.suggested_department == "Public Works"
    db_path.unlink()


def test_request_persistence_api_round_trip(monkeypatch, tmp_path: Path) -> None:
    db_path = tmp_path / "civic311-api.db"
    monkeypatch.setenv("CIVIC311_REQUEST_DB_URL", f"sqlite+pysqlite:///{db_path.as_posix()}")
    _dispose_request_repository()

    created = client.post(
        "/api/v1/civic311/intake",
        json={
            "request_id": "sr-001",
            "category": "street",
            "description": "blocked road hazard",
            "location": "5th Ave",
        },
    )
    fetched = client.get("/api/v1/civic311/intake/sr-001")
    triage = client.post(
        "/api/v1/civic311/triage",
        json={
            "request_id": "sr-001",
            "category": "street",
            "description": "blocked road hazard",
            "location": "5th Ave",
        },
    )
    fetched_triage = client.get("/api/v1/civic311/triage/sr-001")

    _dispose_request_repository()
    monkeypatch.delenv("CIVIC311_REQUEST_DB_URL")

    assert created.status_code == 200
    assert fetched.status_code == 200
    assert fetched.json()["request_id"] == "sr-001"
    assert triage.status_code == 200
    assert triage.json()["request_id"] == "sr-001"
    assert fetched_triage.status_code == 200
    assert fetched_triage.json()["suggested_department"] == "Public Works"
    db_path.unlink()


def test_get_request_without_persistence_returns_actionable_503(monkeypatch) -> None:
    monkeypatch.delenv("CIVIC311_REQUEST_DB_URL", raising=False)
    _dispose_request_repository()

    response = client.get("/api/v1/civic311/intake/sr-001")

    assert response.status_code == 503
    detail = response.json()["detail"]
    assert detail["message"] == "Civic311 request persistence is not configured."
    assert "Set CIVIC311_REQUEST_DB_URL" in detail["fix"]


def test_get_triage_missing_id_returns_actionable_404(monkeypatch, tmp_path: Path) -> None:
    db_path = tmp_path / "civic311-missing.db"
    monkeypatch.setenv("CIVIC311_REQUEST_DB_URL", f"sqlite+pysqlite:///{db_path.as_posix()}")
    _dispose_request_repository()

    response = client.get("/api/v1/civic311/triage/missing")

    _dispose_request_repository()
    monkeypatch.delenv("CIVIC311_REQUEST_DB_URL")

    assert response.status_code == 404
    detail = response.json()["detail"]
    assert detail["message"] == "Triage review record not found."
    assert "POST /api/v1/civic311/triage" in detail["fix"]
    db_path.unlink()
