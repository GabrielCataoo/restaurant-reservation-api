
# Restaurant Reservation BOT – FastAPI + WhatsApp + AWS

This project is a RESTful API developed using FastAPI to manage table reservations for a restaurant that operates exclusively from Thursday to Saturday. The system serves as the backend for a WhatsApp chatbot and is designed to be deployed on AWS EC2 as part of a real-world solution and professional portfolio.

## Features

- Create reservations with name, date, and number of people
- Edit reservations (customer, date, or people count)
- Cancel reservations by ID
- Check available slots for a specific date
- Retrieve a reservation by ID
- Admin-only: list all reservations with access code
- Capacity control: 60 people per day
- Limit per reservation: 20 people max
- Valid only for Thursday to Saturday
- Input validation with Pydantic
- Event logging (create, update, cancel)
- Secure admin access via `.env`
- CORS enabled for potential frontend integration

## Technology Stack

- FastAPI (Web framework)
- SQLite (Local lightweight database)
- SQLAlchemy (ORM)
- Uvicorn (ASGI server)
- Pydantic (Validation)
- Python-dotenv (Environment variables)
- Logging (Monitoring actions)

## Project Structure

```
app/
├── __init__.py
├── main.py            # API routes
├── crud.py            # Business logic
├── database.py        # DB connection and setup
├── models.py          # Booking model
├── schemas.py         # Pydantic schemas
├── utils.py           # Date validation
├── config.py          # Loads admin code from .env
.env                   # Environment variables (not versioned)
requirements.txt       # Dependencies list
```

## Security Notes

- Admin route `/reservations` requires a code via query param: `?admin_code=...`
- Only bookings with correct ID can be edited or deleted
- Admin code is stored securely in `.env`

## Local Testing

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the development server:

```bash
uvicorn app.main:app --reload
```

4. Open your browser at:

```
http://localhost:8000/docs
```

## Production Deployment (EC2)

The API is ready for deployment on AWS EC2 with:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 80
```

You can optionally use Gunicorn and Nginx for production-grade setup.

## WhatsApp Integration

This API is designed to integrate with WhatsApp Cloud API (Meta).  
Incoming messages are parsed and translated into booking actions such as checking availability, creating, or updating reservations.

## Real-World Use Case

This system was built to solve a real operational problem faced by my family's restaurant, which needed an efficient and structured method to manage reservations via WhatsApp. It also serves as a practical showcase of backend and cloud skills for professional purposes.

## Author

Developed by Gabriel Catão  
Available on LinkedIn for professional contact.
