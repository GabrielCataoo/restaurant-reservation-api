from datetime import datetime

def validate_date(date_str):
    try:
        date = datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        print("❌ Formato de data inválido. Use DD/MM/AAAA.")
        return False

    today = datetime.now().date()
    if date.date() < today:
        print("❌ A data não pode estar no passado.")
        return False

    if date.weekday() not in [3, 4, 5]:  # quinta, sexta, sábado
        print("❌ Nós funcionamos de Quinta-feira até Sábado.")
        return False

    return True
