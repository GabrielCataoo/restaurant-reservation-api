from pydantic import BaseModel

class ReservationBase(BaseModel):
    customer: str
    date: str
    people: int

class ReservationCreate(ReservationBase):
    pass

class ReservationUpdate(BaseModel):
    customer: str | None = None
    date: str | None = None
    people: int | None = None

class ReservationOut(ReservationBase):
    id: str

    class Config:
        orm_mode = True
