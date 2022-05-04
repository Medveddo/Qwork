import datetime
from lib2to3.pgen2.token import OP
from typing import Optional

from pydantic import BaseModel


class TextInput(BaseModel):
    text: str

    class Config:
        schema_extra = {
            "example": {
                "text": "Температура 37.9. Давление высокое - 120 на 80."
            }
        }


class RunResult(BaseModel):
    is_correspond: Optional[bool] = None  # TODO: rename -> is_corresponding
    temperature: Optional[float] = None
    systole_pressure: Optional[int] = None
    diastole_pressure: Optional[int] = None
    run_id: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "is_correspond": True,
                "temperature": 37.9,
                "systole_pressure": 120,
                "diastole_pressure": 80,
                "run_id": "095zpx3ZdYMLwGkZ",
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

class Run(BaseModel):
    text: Optional[str]
    is_corresponding: bool
    temperature: Optional[float]
    systole_pressure: Optional[int]
    diastole_pressure: Optional[int]


class Patient(BaseModel):
    id_: int
    full_name: str
    birthdate: datetime.datetime
