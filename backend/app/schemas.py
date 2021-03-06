import datetime
from typing import List, Optional

from pydantic import BaseModel


class TextInput(BaseModel):
    text: str
    type: str

    class Config:
        schema_extra = {
            "example": {
                "text": "Температура 37.9. Давление высокое - 120 на 80. ИМТ 38.09.",
                "type": "all",
            }
        }


class ProcessingRun(BaseModel):
    run_id: str
    finished: bool

    class Config:
        schema_extra = {
            "example": {
                "run_id": "095zpx3ZdYMLwGkZ",
                "finished": False,
            }
        }


class Run(BaseModel):
    is_corresponding: Optional[bool] = None
    text: str
    type: str
    temperature: Optional[float] = None
    systole_pressure: Optional[int] = None
    diastole_pressure: Optional[int] = None
    run_id: Optional[str] = None
    finished: bool

    class Config:
        schema_extra = {
            "example": {
                "is_corresponding": True,
                "type": "acute_coronary_syndrome",
                "temperature": 37.9,
                "systole_pressure": 120,
                "diastole_pressure": 80,
                "run_id": "095zpx3ZdYMLwGkZ",
                "finished": True,
            }
        }


class ResponseWithRunId(BaseModel):
    run_id: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "run_id": "095zpx3ZdYMLwGkZ",
            }
        }


class Patient(BaseModel):
    id_: int
    full_name: str
    birthdate: datetime.datetime


class FeaturesResult(BaseModel):
    found_features: Optional[List[str]] = []
    missing_features: Optional[List[str]] = []


class RunNew(BaseModel):
    text: str
    type: Optional[str]
    result: FeaturesResult
    finished: bool
    run_id: Optional[str] = None
