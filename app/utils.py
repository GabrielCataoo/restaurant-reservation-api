from datetime import datetime

def validate_date(date_str):
    try:
        date = datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        print("❌ Invalid date format. Use DD/MM/YYYY.")
        return False

    today = datetime.now().date()
    if date.date() < today:
        print("❌ The date cannot be in the past.")
        return False

    if date.weekday() not in [3, 4, 5]:  # quinta, sexta, sábado
        print("❌ The establishment only opens Thursday - Saturday.")
        return False

    return True
