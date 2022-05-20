# Cheatsheet inspired by: https://pythonru.com/biblioteki/crud-sqlalchemy-orm

from faker import Faker

from app.database import SessionLocal
from app.models import Patient, Run

fake = Faker("ru_RU")

# Make sure database has all migrations applied
# alembic upgrade head

# Create session with our database
db = SessionLocal()

# Create patient 1
patient = Patient(
    full_name=fake.name(),
    birthdate=fake.date_between(),
)
# print(f"<Patient {patient.id} {patient.full_name} {patient.birthdate}>")
db.add(patient)
# print(f"<Patient {patient.id} {patient.full_name} {patient.birthdate}>")
db.commit()
# print(f"<Patient {patient.id} {patient.full_name} {patient.birthdate}>")
db.refresh(patient)
print(f"<Patient {patient.id} {patient.full_name} {patient.birthdate}>")

# Create patient 2
patient2 = Patient(
    full_name=fake.name(),
    birthdate=fake.date_between(),
)
db.add(patient2)
db.commit()
db.refresh(patient2)
print(f"<Patient {patient2.id} {patient2.full_name} {patient2.birthdate}>")

# Create text run wihtout patient relation
run = Run(
    text=fake.text(max_nb_chars=30),
)
db.add(run)
db.commit()
db.refresh(run)
print(f"<Run#{run.id} {run.text} {run.patient_id}>")

# Create two text runs with relation to patient1, one of patient2
run2 = Run(text=fake.text(max_nb_chars=30), patient_id=patient.id)
run3 = Run(text=fake.text(max_nb_chars=30), patient_id=patient.id)
run4 = Run(text=fake.text(max_nb_chars=30), patient_id=patient2.id)
db.add_all([run2, run3, run4])
db.commit()
for run in (run2, run3, run4):
    run.show_info()

query_set = db.query(Run).filter(Run.patient_id == patient.id).all()
print(f"\nRuns of {patient.full_name}:")
for run in query_set:
    run.show_info()

query_set = db.query(Run).filter(Run.patient_id == patient2.id).all()
print(f"\nRuns of {patient2.full_name}:")
for run in query_set:
    run.show_info()


# Update run text
run3.text = fake.text(max_nb_chars=60)
db.add(run3)
db.commit()
print("\nUpdated run")
run3.show_info()


# Access patient of run
print(run3.patient.full_name)

# Access patient runs
print([run.text for run in patient.text_processes])

db.delete(patient)
db.delete(patient2)

# Delete all runs

db.query(Run).filter(Run.id >= run2.id - 1).delete(  # because run rewrited with for loops (:
    synchronize_session="fetch"
)
db.commit()

# After interacting with database close the connection
db.close()

# Written with models.py:

# from sqlalchemy import (Boolean, Column, Float, ForeignKey,
# Integer, Text, String, DateTime)
# from sqlalchemy.orm import relationship

# from .database import Base


# class Run(Base):
#     __tablename__ = "runs"

#     id = Column(Integer, primary_key=True, index=True)
#     text = Column(Text)
#     is_corresponding = Column(Boolean, default=False)
#     temperature = Column(Float, nullable=True)
#     systole_pressure = Column(Integer, nullable=True)
#     diastole_pressure = Column(Integer, nullable=True)
#     patient_id = Column(Integer, ForeignKey("patients.id"))

#     patient = relationship("Patient", back_populates="text_processes")

#     def show_info(self):
#         print(f"<Run#{self.id} {self.text} {self.patient_id}>")

# class Patient(Base):
#     __tablename__ = "patients"

#     id = Column(Integer, primary_key=True, index=True)
#     full_name = Column(String(length=255))
#     birthdate = Column(DateTime)

#     text_processes = relationship("Run", back_populates="patient")


# with database.py

# import os

# from dotenv import load_dotenv
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# load_dotenv()

# SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()
