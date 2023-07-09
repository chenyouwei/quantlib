from datetime import datetime


def validate_date(date: str, date_format: str) -> bool:
    try:
        time = datetime.strptime(date, date_format)
    except ValueError:
        raise ValueError("")

    return True
