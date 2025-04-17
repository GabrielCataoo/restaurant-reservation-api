
import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_CODE = os.getenv("ADMIN_CODE", "reservationlist")
