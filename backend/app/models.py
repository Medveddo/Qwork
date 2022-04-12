from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from .database import Base


class Run(Base):
    __tablename__ = "runs"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    is_corresponding = Column(Boolean, default=False)
    temperature = Column(Float, nullable=True)
    systole_pressure = Column(Integer, nullable=True)
    diastole_pressure = Column(Integer, nullable=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))

    patient = relationship("Patient", back_populates="text_processes")

    def show_info(self):
        print(f"<Run#{self.id} {self.text} {self.patient_id}>")


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(length=255))
    birthdate = Column(DateTime)

    text_processes = relationship("Run", back_populates="patient")
