import json
from datetime import datetime, timedelta

def load_holidays(file_path='holidays.json'):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def is_business_day(date, holidays, comarca=None):
    # Check for weekend
    if date.weekday() >= 5:  # Saturday (5) or Sunday (6)
        return False

    # Check for national/state holidays and recess
    for holiday in holidays:
        holiday_date = datetime.strptime(holiday['date'], '%Y-%m-%d').date()
        if date == holiday_date:
            if holiday['scope'] == 'Nacional/Estadual':
                return False
            # Check for municipal holidays if comarca is specified
            if comarca and holiday['scope'].lower() == comarca.lower():
                return False
    return True

def calculate_judicial_deadline(start_date_str, num_days, comarca=None, holidays_file='holidays.json'):
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    holidays = load_holidays(holidays_file)

    current_date = start_date
    business_days_counted = 0

    while business_days_counted < num_days:
        current_date += timedelta(days=1)
        if is_business_day(current_date, holidays, comarca):
            business_days_counted += 1

    return current_date.strftime('%Y-%m-%d')

if __name__ == '__main__':
    # Example Usage:
    # Assuming today is 2025-07-17 and a 5-day deadline for Fortaleza
    start_date = '2025-07-17'
    num_days = 5
    comarca = 'Fortaleza'
    deadline = calculate_judicial_deadline(start_date, num_days, comarca)
    print(f"O prazo de {num_days} dias úteis, iniciando em {start_date} para a comarca de {comarca}, vence em: {deadline}")

    # Example with a national holiday (e.g., Nov 20, 2025 - Consciência Negra)
    start_date_national = '2025-11-17'
    num_days_national = 3
    deadline_national = calculate_judicial_deadline(start_date_national, num_days_national)
    print(f"O prazo de {num_days_national} dias úteis, iniciando em {start_date_national} (nacional), vence em: {deadline_national}")

    # Example with recess (Dec 20, 2025 to Jan 06, 2026)
    start_date_recess = '2025-12-18'
    num_days_recess = 5
    deadline_recess = calculate_judicial_deadline(start_date_recess, num_days_recess)
    print(f"O prazo de {num_days_recess} dias úteis, iniciando em {start_date_recess} (recesso), vence em: {deadline_recess}")


