
import uuid
from sqlalchemy.orm import Session
from . import models, schemas
from .utils import validate_date

MAX_PEOPLE_PER_DAY = 60
MAX_PEOPLE_PER_BOOKING = 20

def total_people_on_day(db: Session, date: str):
    return sum(b.people for b in db.query(models.Reservation).filter(models.Reservation.date == date).all())

def create_reservation(db: Session, reservation: schemas.ReservationCreate):
    if reservation.people > MAX_PEOPLE_PER_BOOKING:
        raise ValueError(f"Max people allowed per reservation: {MAX_PEOPLE_PER_BOOKING}")

    if not validate_date(reservation.date):
        raise ValueError("Invalid date or format. Please use DD/MM/YYYY and valid reservation days.")

    total = total_people_on_day(db, reservation.date)
    if total + reservation.people > MAX_PEOPLE_PER_DAY:
        raise ValueError(f"Capacity exceeded for this date. Only {MAX_PEOPLE_PER_DAY - total} spots remaining.")

    reservation_id = str(uuid.uuid4())[:5]
    new_reservation = models.Reservation(
        id=reservation_id,
        customer=reservation.customer,
        date=reservation.date,
        people=reservation.people
    )
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    return new_reservation

def list_reservations(db: Session):
    return db.query(models.Reservation).all()

def get_reservation(db: Session, reservation_id: str):
    return db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()

def delete_reservation(db: Session, reservation_id: str):
    reservation = get_reservation(db, reservation_id)
    if reservation:
        db.delete(reservation)
        db.commit()
        return True
    return False

def update_reservation(db: Session, reservation_id: str, data: schemas.ReservationUpdate):
    reservation = get_reservation(db, reservation_id)
    if not reservation:
        return None

    new_date = data.date if data.date else reservation.date
    new_people = data.people if data.people is not None else reservation.people

    if new_people > MAX_PEOPLE_PER_BOOKING:
        raise ValueError(f"Max people allowed per reservation: {MAX_PEOPLE_PER_BOOKING}")

    if not validate_date(new_date):
        raise ValueError("Invalid date or format. Please use DD/MM/YYYY and valid reservation days.")

    existing_people = total_people_on_day(db, new_date)
    if new_date == reservation.date:
        existing_people -= reservation.people

    if existing_people + new_people > MAX_PEOPLE_PER_DAY:
        raise ValueError(f"Capacity exceeded for this date. Only {MAX_PEOPLE_PER_DAY - existing_people} spots remaining.")

    if data.customer is not None:
        reservation.customer = data.customer
    reservation.date = new_date
    reservation.people = new_people

    db.commit()
    db.refresh(reservation)
    return reservation
