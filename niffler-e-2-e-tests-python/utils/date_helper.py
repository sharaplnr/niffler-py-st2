from datetime import datetime

def format_date(iso_date: str) -> str:
    dt = datetime.strptime(iso_date, '%Y-%m-%dT%H:%M:%S.%f%z')
    formatted_date = dt.strftime('%b %d, %Y')
    return formatted_date