from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_health_reports_operational_model() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["model_version"] == "v7"


def test_predict_rejects_input_without_clinical_signal() -> None:
    response = client.post("/predict", json={"age": 72, "gender": "Female"})

    assert response.status_code == 422
    assert "chief complaint or vital sign" in response.json()["detail"]


def test_predict_accepts_three_field_sparse_input() -> None:
    response = client.post(
        "/predict",
        json={
            "chief_complaint": "chestpain",
            "heart_rate": 112,
            "oxygen_saturation": 91,
        },
    )

    assert response.status_code == 200
    result = response.json()
    assert result["model_version"] == "v7"
    assert result["data_completeness"] < 1
    assert result["missing_recommended_fields"]
