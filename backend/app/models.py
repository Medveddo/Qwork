from sqlalchemy import JSON, Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class RunNew(Base):
    __tablename__ = "runs_new"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    type = Column(String(length=30))
    result = Column(JSON, default={})
    finished = Column(Boolean, default=False)


class Run(Base):
    __tablename__ = "runs"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    is_corresponding = Column(Boolean, default=False)
    temperature = Column(Float, nullable=True)
    systole_pressure = Column(Integer, nullable=True)
    diastole_pressure = Column(Integer, nullable=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    finished = Column(Boolean, default=False)
    type = Column(String(length=30))

    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), onupdate=func.now())

    patient = relationship("Patient", back_populates="text_processes")

    def show_info(self):
        print(f"<Run#{self.id} {self.text} {self.patient_id}>")


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(length=255))
    birthdate = Column(DateTime)

    text_processes = relationship("Run", back_populates="patient")
