from sqlalchemy import Boolean, Column, Float, Integer, Text

from .database import Base


class TextProcessResult(Base):
    __tablename__ = "text_process_result"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    is_corresponding = Column(Boolean, default=False)
    temperature = Column(Float, nullable=True)
    systole_pressure = Column(Integer, nullable=True)
    diastole_pressure = Column(Integer, nullable=True)
