from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine, Base
from .utils import validate_date
from .config import ADMIN_CODE
from fastapi.middleware.cors import CORSMiddleware
import logging

Base.metadata.create_all(bind=engine)

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CORS enabled for demonstration and future frontend compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to trusted domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/reservation", response_model=schemas.ReservationOut)
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    try:
        new = crud.create_reservation(db, reservation)
        logger.info(f"✅ Reservation created: ID={new.id}, Customer={new.customer}, Date={new.date}, People={new.people}")
        return new
    except ValueError as e:
        logger.error(f"Error creating reservation: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/reservations", response_model=list[schemas.ReservationOut])
def list_reservations(admin_code: str = Query(...), db: Session = Depends(get_db)):
    if admin_code != ADMIN_CODE:
        raise HTTPException(status_code=401, detail="Unauthorized access")
    return crud.list_reservations(db)

@app.get("/reservation/{id}", response_model=schemas.ReservationOut)
def get_reservation(id: str, db: Session = Depends(get_db)):
    reservation = crud.get_reservation(db, id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

@app.put("/reservation/{id}", response_model=schemas.ReservationOut)
def update_reservation(id: str, date: schemas.ReservationUpdate, db: Session = Depends(get_db)):
    try:
        reservation = crud.update_reservation(db, id, date)
    except ValueError as e:
        logger.error(f"Error updating reservation {id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    logger.info(f"✏️ Reservation updated: ID={reservation.id}, Customer={reservation.customer}, Date={reservation.date}, People={reservation.people}")
    return reservation

@app.delete("/reservation/{id}")
def delete_reservation(id: str, db: Session = Depends(get_db)):
    ok = crud.delete_reservation(db, id)
    if not ok:
        raise HTTPException(status_code=404, detail="Reservation not found")
    logger.warning(f"❌ Reservation cancelled: ID={id}")
    return {"message": "Reservation successfully cancelled"}

@app.get("/availability")
def check_availability(date: str = Query(..., example="12/04/2025"), db: Session = Depends(get_db)):
    if not validate_date(date):
        raise HTTPException(status_code=400, detail="Data inválida ou fora dos operating days")
    total = sum(b.people for b in db.query(models.Reservation).filter(models.Reservation.date == date).all())
    slots = 60 - total
    return {"date": date, "available_slots": slots}
