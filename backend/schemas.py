from typing import Optional

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class PatientInput(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    age: Optional[float] = Field(None, ge=0, le=120)
    gender: Optional[str] = "missing"
    arrivalmode: Optional[str] = Field(
        "Walk-in",
        validation_alias=AliasChoices("arrivalmode", "arrival_mode"),
    )
    arrivalmonth: Optional[str] = "missing"
    arrivalday: Optional[str] = "missing"
    arrivalhour_bin: Optional[str] = "missing"
    previous_ed_visits: Optional[int] = Field(None, ge=0)
    previous_admissions: Optional[int] = Field(None, ge=0)
    previous_surgeries: Optional[int] = Field(None, ge=0)
    previousdispo: Optional[str] = "No previous dispo"
    chief_complaint: Optional[str] = None
    history_conditions: list[str] = Field(default_factory=list)
    heart_rate: Optional[float] = Field(None, ge=0, le=260)
    systolic_bp: Optional[float] = Field(
        None,
        ge=0,
        le=300,
        validation_alias=AliasChoices("systolic_bp", "systolic_blood_pressure"),
    )
    diastolic_bp: Optional[float] = Field(
        None,
        ge=0,
        le=200,
        validation_alias=AliasChoices("diastolic_bp", "diastolic_blood_pressure"),
    )
    respiratory_rate: Optional[float] = Field(None, ge=0, le=80)
    oxygen_saturation: Optional[float] = Field(None, ge=0, le=100)
    temperature: Optional[float] = Field(
        None,
        ge=20,
        le=45,
        validation_alias=AliasChoices("temperature", "body_temperature"),
    )
    oxygen_device: Optional[int] = 0


class PredictionOutput(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    model_version: str
    operational_mode: str
    operating_profile: str
    model_probability: float
    critical_probability: float
    threshold: float
    risk_level: str
    triage_band: str
    recommended_action: str
    explanation: list[str]
    safety_flags: list[str]
    next_best_actions: list[str]
    safety_override: bool
    safety_severity: str
    assessment_basis: str
    safety_rule_version: str
    measurement_warnings: list[str]
    out_of_distribution: bool
    data_completeness: float
    confidence_band: str
    missing_recommended_fields: list[str]
    disclaimer: str


class StakeholderFeedbackInput(BaseModel):
    stakeholder_type: str = Field(..., min_length=2, max_length=80)
    understandability: int = Field(..., ge=1, le=5)
    ui_clarity: int = Field(..., ge=1, le=5)
    disclaimer_clarity: int = Field(..., ge=1, le=5)
    comment: str = Field(..., min_length=2, max_length=1000)


class StakeholderFeedbackOutput(BaseModel):
    status: str
    stored_count: int
    export_path: str
