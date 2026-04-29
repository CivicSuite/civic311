from fastapi.testclient import TestClient

import civic311
from civic311.main import app


client = TestClient(app)


def test_package_version_is_011() -> None:
    assert civic311.__version__ == "0.1.1"


def test_root_endpoint_states_runtime_boundary() -> None:
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Civic311"
    assert data["status"] == "resident service request foundation plus request persistence"
    assert "database-backed service request and triage review records" in data["message"]
    assert "official dispatch" in data["message"]
    assert "Post-v0.1.1 roadmap" in data["next_step"]


def test_health_endpoint_reports_versions() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "civic311"
    assert data["version"] == "0.1.1"
    assert data["civiccore_version"] == "0.3.0"
