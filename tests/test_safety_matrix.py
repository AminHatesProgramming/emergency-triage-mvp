import random

import pytest

from ml.inference import TriagePredictor, normalize_chief_complaint


SEVERITY_RANK = {"none": 0, "urgent": 1, "immediate": 2}


@pytest.mark.parametrize(
    ("patient", "expected_severity"),
    [
        ({"age": 30, "heart_rate": 90}, "none"),
        ({"age": 30, "heart_rate": 110}, "none"),
        ({"age": 30, "heart_rate": 111}, "urgent"),
        ({"age": 30, "heart_rate": 129}, "urgent"),
        ({"age": 30, "heart_rate": 130}, "urgent"),
        ({"age": 30, "heart_rate": 149}, "urgent"),
        ({"age": 30, "heart_rate": 150}, "immediate"),
        ({"age": 30, "heart_rate": 50}, "urgent"),
        ({"age": 30, "heart_rate": 39}, "immediate"),
        ({"age": 30, "systolic_bp": 101}, "none"),
        ({"age": 30, "systolic_bp": 100}, "urgent"),
        ({"age": 30, "systolic_bp": 91}, "urgent"),
        ({"age": 30, "systolic_bp": 90}, "immediate"),
        ({"age": 30, "systolic_bp": 220}, "urgent"),
        ({"age": 30, "respiratory_rate": 12}, "none"),
        ({"age": 30, "respiratory_rate": 11}, "urgent"),
        ({"age": 30, "respiratory_rate": 8}, "immediate"),
        ({"age": 30, "respiratory_rate": 20}, "none"),
        ({"age": 30, "respiratory_rate": 21}, "urgent"),
        ({"age": 30, "respiratory_rate": 29}, "urgent"),
        ({"age": 30, "respiratory_rate": 30}, "immediate"),
        ({"age": 30, "oxygen_saturation": 94}, "none"),
        ({"age": 30, "oxygen_saturation": 93}, "urgent"),
        ({"age": 30, "oxygen_saturation": 90}, "urgent"),
        ({"age": 30, "oxygen_saturation": 89}, "immediate"),
        ({"age": 30, "temperature": 36.0}, "none"),
        ({"age": 30, "temperature": 35.9}, "urgent"),
        ({"age": 30, "temperature": 35.0}, "immediate"),
        ({"age": 30, "temperature": 39.1}, "urgent"),
        ({"age": 30, "temperature": 40.0}, "immediate"),
    ],
)
def test_adult_safety_boundaries(patient: dict, expected_severity: str) -> None:
    assert TriagePredictor.safety_assessment(patient)["severity"] == expected_severity


@pytest.mark.parametrize(
    ("age", "heart_rate", "expected_severity"),
    [
        (0.5, 149, "none"),
        (0.5, 150, "urgent"),
        (0.5, 219, "urgent"),
        (0.5, 220, "immediate"),
        (1, 139, "none"),
        (1, 140, "urgent"),
        (3, 129, "none"),
        (3, 130, "urgent"),
        (5, 119, "none"),
        (5, 120, "urgent"),
        (5, 150, "urgent"),
        (5, 180, "immediate"),
        (6, 109, "none"),
        (6, 110, "urgent"),
        (8, 104, "none"),
        (8, 105, "urgent"),
        (12, 110, "none"),
        (12, 111, "urgent"),
        (15.9, 130, "urgent"),
        (16, 130, "urgent"),
    ],
)
def test_age_adjusted_heart_rate_boundaries(
    age: float, heart_rate: float, expected_severity: str
) -> None:
    result = TriagePredictor.safety_assessment({"age": age, "heart_rate": heart_rate})

    assert result["severity"] == expected_severity
    if age < 16:
        assert "adult heart rate" not in " ".join(result["flags"])


@pytest.mark.parametrize(
    ("age", "respiratory_rate", "expected_severity"),
    [
        (0.5, 49, "none"),
        (0.5, 50, "urgent"),
        (0.5, 70, "immediate"),
        (1, 39, "none"),
        (1, 40, "urgent"),
        (1, 60, "immediate"),
        (3, 34, "none"),
        (3, 35, "urgent"),
        (3, 60, "immediate"),
        (5, 23, "none"),
        (5, 24, "urgent"),
        (5, 50, "immediate"),
        (6, 23, "none"),
        (6, 24, "urgent"),
        (6, 50, "immediate"),
        (8, 21, "none"),
        (8, 22, "urgent"),
        (8, 45, "immediate"),
        (12, 20, "none"),
        (12, 21, "urgent"),
        (12, 40, "immediate"),
    ],
)
def test_age_adjusted_respiratory_rate_boundaries(
    age: float, respiratory_rate: float, expected_severity: str
) -> None:
    result = TriagePredictor.safety_assessment(
        {"age": age, "respiratory_rate": respiratory_rate}
    )

    assert result["severity"] == expected_severity


@pytest.mark.parametrize(
    ("age", "systolic_bp", "expected_severity"),
    [
        (0.5, 70, "none"),
        (0.5, 69, "immediate"),
        (1, 72, "none"),
        (1, 71, "immediate"),
        (5, 80, "none"),
        (5, 79, "immediate"),
        (10, 90, "none"),
        (10, 89, "immediate"),
        (12, 90, "none"),
        (12, 89, "immediate"),
    ],
)
def test_pediatric_hypotension_boundaries(
    age: float, systolic_bp: float, expected_severity: str
) -> None:
    result = TriagePredictor.safety_assessment({"age": age, "systolic_bp": systolic_bp})

    assert result["severity"] == expected_severity


@pytest.mark.parametrize(
    ("patient", "expected_severity"),
    [
        ({"age": 0.20, "temperature": 37.9}, "none"),
        ({"age": 0.20, "temperature": 38.0}, "immediate"),
        ({"age": 0.40, "temperature": 38.9}, "none"),
        ({"age": 0.40, "temperature": 39.0}, "urgent"),
        ({"age": 0.50, "temperature": 39.0}, "none"),
    ],
)
def test_infant_fever_boundaries(patient: dict, expected_severity: str) -> None:
    assert TriagePredictor.safety_assessment(patient)["severity"] == expected_severity


@pytest.mark.parametrize(
    ("patient", "expected_severity", "expected_fragment"),
    [
        (
            {"age": 40, "heart_rate": 120, "systolic_bp": 100},
            "immediate",
            "shock index",
        ),
        (
            {"age": 40, "heart_rate": 100, "systolic_bp": 100},
            "urgent",
            "shock index",
        ),
        (
            {"age": 40, "oxygen_saturation": 91, "heart_rate": 111, "respiratory_rate": 25},
            "immediate",
            "combined adult vital-sign score",
        ),
        (
            {"age": 5, "heart_rate": 130, "respiratory_rate": 29},
            "immediate",
            "multiple age-adjusted pediatric vital signs",
        ),
    ],
)
def test_combined_vital_sign_escalation(
    patient: dict, expected_severity: str, expected_fragment: str
) -> None:
    result = TriagePredictor.safety_assessment(patient)

    assert result["severity"] == expected_severity
    assert expected_fragment in " ".join(result["flags"])


@pytest.mark.parametrize(
    "patient",
    [
        {"age": 30, "heart_rate": 260},
        {"age": 30, "oxygen_saturation": 42},
        {"age": 30, "systolic_bp": 35},
        {"age": 30, "respiratory_rate": 75},
        {"age": 30, "temperature": 44},
        {"age": 30, "systolic_bp": 100, "diastolic_bp": 105},
        {"age": 30, "systolic_bp": 100, "diastolic_bp": 95},
    ],
)
def test_implausible_measurements_are_marked_for_verification(patient: dict) -> None:
    result = TriagePredictor.safety_assessment(patient)

    assert result["out_of_distribution"] is True
    assert result["measurement_warnings"]


@pytest.mark.parametrize(
    ("value", "age", "expected"),
    [
        ("fever", 30, "cc_fever-9weeksto74years"),
        ("headache", 30, "cc_headache-newonsetornewsymptoms"),
        ("headache-new onset or new symptoms", 30, "cc_headache-newonsetornewsymptoms"),
        ("fall", 64, "cc_fall"),
        ("fall", 65, "cc_fall>65"),
        ("shortness of breath", 30, "cc_shortnessofbreath"),
    ],
)
def test_ui_complaints_map_to_real_model_features(value: str, age: float, expected: str) -> None:
    assert normalize_chief_complaint(value, age) == expected


def test_normal_reference_cases_do_not_trigger_deterministic_escalation() -> None:
    reference_cases = [
        {"age": 0.5, "heart_rate": 120, "systolic_bp": 80, "respiratory_rate": 35, "oxygen_saturation": 97, "temperature": 37},
        {"age": 5, "heart_rate": 100, "systolic_bp": 95, "respiratory_rate": 20, "oxygen_saturation": 97, "temperature": 37},
        {"age": 12, "heart_rate": 90, "systolic_bp": 105, "respiratory_rate": 18, "oxygen_saturation": 97, "temperature": 37},
        {"age": 30, "heart_rate": 75, "systolic_bp": 120, "diastolic_bp": 80, "respiratory_rate": 16, "oxygen_saturation": 98, "temperature": 36.8},
        {"age": 80, "heart_rate": 80, "systolic_bp": 130, "diastolic_bp": 75, "respiratory_rate": 18, "oxygen_saturation": 96, "temperature": 36.5},
    ]

    for patient in reference_cases:
        result = TriagePredictor.safety_assessment(patient)
        assert result["severity"] == "none"
        assert result["out_of_distribution"] is False


def test_high_side_adult_boundaries_are_monotonic() -> None:
    values = [90, 100, 110, 111, 129, 130, 149, 150, 180, 220]
    ranks = [
        SEVERITY_RANK[TriagePredictor.safety_assessment({"age": 35, "heart_rate": value})["severity"]]
        for value in values
    ]

    assert ranks == sorted(ranks)


def test_falling_oxygen_saturation_never_reduces_severity() -> None:
    values = [100, 96, 95, 94, 93, 90, 89, 80, 50]
    ranks = [
        SEVERITY_RANK[
            TriagePredictor.safety_assessment({"age": 35, "oxygen_saturation": value})["severity"]
        ]
        for value in values
    ]

    assert ranks == sorted(ranks)


def test_seeded_broad_input_grid_never_crashes_or_returns_invalid_shape() -> None:
    randomizer = random.Random(20260716)
    for _ in range(5000):
        patient = {
            "age": randomizer.choice([None, 0.1, 0.4, 1, 3, 5, 8, 12, 15.9, 16, 30, 65, 90]),
            "heart_rate": randomizer.choice([None, 20, 39, 40, 50, 60, 90, 110, 111, 130, 149, 150, 180, 220, 250]),
            "systolic_bp": randomizer.choice([None, 40, 69, 70, 79, 80, 89, 90, 100, 110, 120, 220, 260]),
            "diastolic_bp": randomizer.choice([None, 20, 40, 60, 80, 100, 160]),
            "respiratory_rate": randomizer.choice([None, 3, 8, 9, 11, 12, 20, 21, 25, 29, 30, 40, 60, 70]),
            "oxygen_saturation": randomizer.choice([None, 50, 80, 89, 90, 93, 94, 95, 96, 100]),
            "temperature": randomizer.choice([None, 30, 35, 35.9, 36, 38, 39, 39.1, 40, 43]),
        }
        result = TriagePredictor.safety_assessment(patient)

        assert result["severity"] in SEVERITY_RANK
        assert isinstance(result["flags"], list)
        assert len(result["flags"]) <= 5
        assert isinstance(result["measurement_warnings"], list)
        assert len(result["measurement_warnings"]) <= 3
        assert result["out_of_distribution"] == bool(result["measurement_warnings"])
