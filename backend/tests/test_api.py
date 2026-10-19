from fastapi.testclient import TestClient

from backend.main import app


def test_health_and_material_catalog() -> None:
    client = TestClient(app)
    with client:
        _test_health_and_material_catalog(client)


def _test_health_and_material_catalog(client: TestClient) -> None:
    health = client.get("/api/v1/health")
    assert health.status_code == 200
    assert health.json()["database"] == "ok"

    materials = client.get("/api/v1/materials")
    assert materials.status_code == 200
    assert any(item["name"] == "Carbon fibre / epoxy" for item in materials.json())
    assert health.headers["x-content-type-options"] == "nosniff"
    assert health.headers["x-frame-options"] == "DENY"


def test_material_detail_and_simulation() -> None:
    client = TestClient(app)
    with client:
        _test_material_detail_and_simulation(client)


def _test_material_detail_and_simulation(client: TestClient) -> None:
    detail = client.get("/api/v1/materials/Carbon fibre / epoxy")
    assert detail.status_code == 200
    assert detail.json()["density_kg_m3"] == 1550

    response = client.post(
        "/api/v1/simulations",
        json={
            "material_name": "Carbon fibre / epoxy",
            "fibre_volume_fraction": 0.6,
            "reference_temperature_k": 293.15,
            "operating_temperature_k": 353.15,
            "laminate": {"angles_deg": [0, 90, 90, 0], "ply_thickness_m": 0.000125},
        },
    )
    assert response.status_code == 201
    payload = response.json()
    assert payload["delta_temperature_k"] == 60
    assert payload["record_id"] > 0
    assert payload["laminate"]["a_matrix"]


def test_invalid_simulation_is_rejected() -> None:
    client = TestClient(app)
    with client:
        _test_invalid_simulation_is_rejected(client)


def _test_invalid_simulation_is_rejected(client: TestClient) -> None:
    response = client.post(
        "/api/v1/simulations",
        json={
            "material_name": "Unknown",
            "fibre_volume_fraction": 0.5,
            "reference_temperature_k": 293.15,
            "operating_temperature_k": 353.15,
        },
    )
    assert response.status_code == 422


def test_saved_simulations_are_listed() -> None:
    client = TestClient(app)
    with client:
        created = client.post(
            "/api/v1/simulations",
            json={
                "material_name": "Carbon fibre / epoxy",
                "fibre_volume_fraction": 0.6,
                "reference_temperature_k": 293.15,
                "operating_temperature_k": 303.15,
            },
        )
        assert created.status_code == 201
        records = client.get("/api/v1/simulations")
        assert records.status_code == 200
        assert records.json()[0]["id"] == created.json()["record_id"]


def test_taxonomy_and_model_compatibility_are_explicit() -> None:
    client = TestClient(app)
    with client:
        taxonomy = client.get("/api/v1/taxonomy")
        assert taxonomy.status_code == 200
        payload = taxonomy.json()
        assert any(item["key"] == "ceramic_matrix" and not item["implemented"] for item in payload["families"])
        assert any(item["key"] == "clt" and item["implemented"] for item in payload["models"])

        supported = client.get("/api/v1/compatibility/fibre_reinforced_polymer/clt")
        assert supported.json()["compatible"] is True
        unsupported = client.get("/api/v1/compatibility/ceramic_matrix/clt")
        assert unsupported.json()["compatible"] is False
