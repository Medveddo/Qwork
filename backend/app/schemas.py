import datetime
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
