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
    assert result["operating_profile"] == "validated_sparse_3"
    assert result["threshold"] == 0.16415970027446747


def test_four_field_validated_sparse_profile_uses_validation_selected_threshold() -> None:
    response = client.post(
        "/predict",
        json={
            "chief_complaint": "chestpain",
            "age": 63,
            "heart_rate": 112,
            "oxygen_saturation": 91,
        },
    )

    assert response.status_code == 200
    result = response.json()
    assert result["operating_profile"] == "validated_sparse_4"
    assert result["threshold"] == 0.1881568878889084


def test_unvalidated_vitals_only_pattern_keeps_default_threshold() -> None:
    response = client.post(
        "/predict",
        json={
            "age": 30,
            "heart_rate": 78,
            "systolic_bp": 120,
            "diastolic_bp": 80,
            "respiratory_rate": 16,
            "oxygen_saturation": 98,
            "temperature": 36.8,
        },
    )

    assert response.status_code == 200
    result = response.json()
    assert result["operating_profile"] == "full_v7_default"
    assert result["threshold"] == 0.3016650974750519


def test_adult_heart_rate_150_triggers_immediate_safety_priority() -> None:
    response = client.post(
        "/predict",
        json={
            "age": 30,
            "heart_rate": 150,
            "systolic_bp": 120,
            "diastolic_bp": 80,
            "respiratory_rate": 16,
            "oxygen_saturation": 98,
            "temperature": 36.8,
        },
    )

    assert response.status_code == 200
    result = response.json()
    assert result["risk_level"] == "critical"
    assert result["safety_severity"] == "immediate"
    assert "adult heart rate at or above 150/min" in " ".join(result["safety_flags"])
    assert result["critical_probability"] == result["model_probability"]


def test_adult_heart_rate_140_is_an_urgent_safety_prompt() -> None:
    response = client.post("/predict", json={"age": 30, "heart_rate": 140})

    assert response.status_code == 200
    result = response.json()
    assert result["safety_severity"] == "urgent"
    assert "130 and 149/min" in " ".join(result["safety_flags"])


def test_child_heart_rate_150_does_not_use_adult_immediate_threshold() -> None:
    response = client.post("/predict", json={"age": 5, "heart_rate": 150})

    assert response.status_code == 200
    result = response.json()
    assert result["safety_severity"] == "urgent"
    assert "child heart rate" in " ".join(result["safety_flags"])
    assert "adult heart rate" not in " ".join(result["safety_flags"])


def test_extreme_measurement_is_not_silently_trusted() -> None:
    response = client.post("/predict", json={"age": 30, "heart_rate": 260})

    assert response.status_code == 200
    result = response.json()
    assert result["risk_level"] == "critical"
    assert result["out_of_distribution"] is True
    assert "heart rate" in " ".join(result["measurement_warnings"])


def test_common_api_aliases_are_accepted_without_dropping_vitals() -> None:
    response = client.post(
        "/predict",
        json={
            "age": 30,
            "arrival_mode": "Walk-in",
            "heart_rate": 150,
            "systolic_blood_pressure": 120,
            "diastolic_blood_pressure": 80,
            "body_temperature": 37,
        },
    )

    assert response.status_code == 200
    result = response.json()
    assert result["safety_severity"] == "immediate"
    assert "systolic blood pressure" not in result["missing_recommended_fields"]
    assert "diastolic blood pressure" not in result["missing_recommended_fields"]
    assert "temperature" not in result["missing_recommended_fields"]


def test_unknown_patient_field_is_rejected_instead_of_silently_ignored() -> None:
    response = client.post(
        "/predict",
        json={"age": 30, "heart_rate": 150, "unknown_vital": 1},
    )

    assert response.status_code == 422
