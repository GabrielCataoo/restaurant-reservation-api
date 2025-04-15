from sqlalchemy import Column, Integer, String
from .database import Base

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(String, primary_key=True, index=True)
    customer = Column(String, nullable=False)
    date = Column(String, nullable=False)
    people = Column(Integer, nullable=False)
