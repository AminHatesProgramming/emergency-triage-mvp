from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PatientInput(BaseModel):
    age: Optional[float] = Field(None, ge=0, le=120)
    gender: Optional[str] = "missing"
    arrivalmode: Optional[str] = "Walk-in"
    arrivalmonth: Optional[str] = "missing"
    arrivalday: Optional[str] = "missing"
    arrivalhour_bin: Optional[str] = "missing"
    previous_ed_visits: int = Field(0, ge=0)
    previous_admissions: int = Field(0, ge=0)
    previous_surgeries: int = Field(0, ge=0)
    previousdispo: Optional[str] = "No previous dispo"
    chief_complaint: Optional[str] = None
    history_conditions: list[str] = Field(default_factory=list)
    heart_rate: Optional[float] = Field(None, ge=0, le=260)
    systolic_bp: Optional[float] = Field(None, ge=0, le=300)
    diastolic_bp: Optional[float] = Field(None, ge=0, le=200)
    respiratory_rate: Optional[float] = Field(None, ge=0, le=80)
    oxygen_saturation: Optional[float] = Field(None, ge=0, le=100)
    temperature: Optional[float] = Field(None, ge=20, le=45)
    oxygen_device: Optional[int] = 0


class PredictionOutput(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    model_version: str
    critical_probability: float
    threshold: float
    risk_level: str
    recommended_action: str
    explanation: list[str]
    data_completeness: float
    confidence_band: str
    missing_recommended_fields: list[str]
    disclaimer: str
