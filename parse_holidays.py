import re
import json
from datetime import datetime, timedelta

def parse_holiday_data(file_path):
    holidays = []
    
    month_mapping = {
        'MARÇO': 3, 'ABRIL': 4, 'MAIO': 5, 'JUNHO': 6, 'JULHO': 7, 'AGOSTO': 8,
        'SETEMBRO': 9, 'OUTUBRO': 10, 'NOVEMBRO': 11, 'DEZEMBRO': 12, 'JANEIRO': 1
    }

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Process national and state holidays
    national_state_section_match = re.search(r"FERIADOS E PONTOS FACULTATIVOS NACIONAIS E ESTADUAIS, ENTRE MARÇO DE 2025 E JANEIRO DE 2026\n(.*?)(?=FERIADOS E PONTOS FACULTATIVOS INCLUSIVE NO ÂMBITO DO MUNICÍPIO DE FORTALEZA, ENTRE MARÇO DE 2025 E JANEIRO DE 2026)", content, re.DOTALL)
    if national_state_section_match:
        section_content = national_state_section_match.group(1).strip()
        lines = section_content.split('\n')
        current_year = 2025 # Default for this section
        for line in lines:
            line = line.strip()
            if not line.startswith('- '):
                continue
            
            month_match = re.match(r'^- ([A-ZÇ]+)(?:/(\d{4}))?:\s*(.*)', line)
            if month_match:
                month_name = month_match.group(1).strip()
                year_in_header = month_match.group(2)
                holiday_details = month_match.group(3).strip()

                if year_in_header:
                    current_year = int(year_in_header)
                elif month_name == "DEZEMBRO":
                    current_year = 2025
                elif month_name == "JANEIRO":
                    current_year = 2026

                month_num = month_mapping.get(month_name.upper())
                if not month_num:
                    continue

                # Split by '), ' to handle multiple holidays in one line
                for detail_part in holiday_details.split('), '):
                    detail_part = detail_part.strip()
                    if not detail_part:
                        continue
                    # Add back the closing parenthesis if it was split off
                    if not detail_part.endswith(')'):
                        detail_part += ')'

                    holiday_pattern = re.compile(r'(\d{1,2}(?: e \d{1,2})?|\d{1,2}/\d{1,2}/\d{4}\s*a\s*\d{1,2}/\d{1,2}/\d{4})\s*\((.*?)\)')
                    holiday_match = holiday_pattern.match(detail_part)
                    
                    if holiday_match:
                        days_str = holiday_match.group(1)
                        description = holiday_match.group(2).strip()

                        if ' a ' in days_str: # Range of dates
                            if '/' in days_str: # Full date format: DD/MM/YYYY a DD/MM/YYYY
                                start_date_str, end_date_str = days_str.split(' a ')
                                start_date = datetime.strptime(start_date_str, '%d/%m/%Y')
                                end_date = datetime.strptime(end_date_str, '%d/%m/%Y')
                            else: # Day range within the same month
                                start_day, end_day = map(int, days_str.split(' a '))
                                start_date = datetime(current_year, month_num, start_day)
                                end_date = datetime(current_year, month_num, end_day)

                            delta = end_date - start_date
                            for j in range(delta.days + 1):
                                date = start_date + timedelta(days=j)
                                holidays.append({
                                    'date': date.strftime('%Y-%m-%d'),
                                    'description': description,
                                    'type': 'Recesso' if 'Recesso' in description else 'Ponto Facultativo' if 'Ponto facultativo' in description else 'Feriado',
                                    'scope': 'Nacional/Estadual'
                                })
                        elif ' e ' in days_str: # Multiple days in the same month
                            days = [int(d) for d in days_str.split(' e ')]
                            for day in days:
                                holidays.append({
                                    'date': datetime(current_year, month_num, day).strftime('%Y-%m-%d'),
                                    'description': description,
                                    'type': 'Ponto Facultativo' if 'Ponto facultativo' in description else 'Feriado',
                                    'scope': 'Nacional/Estadual'
                                })
                        else: # Single day
                            day = int(days_str)
                            holidays.append({
                                'date': datetime(current_year, month_num, day).strftime('%Y-%m-%d'),
                                'description': description,
                                'type': 'Ponto Facultativo' if 'Ponto facultativo' in description else 'Feriado',
                                'scope': 'Nacional/Estadual'
                            })

    # Process Fortaleza specific holidays
    fortaleza_section_match = re.search(r"FERIADOS E PONTOS FACULTATIVOS INCLUSIVE NO ÂMBITO DO MUNICÍPIO DE FORTALEZA, ENTRE MARÇO DE 2025 E JANEIRO DE 2026\n(.*?)(?=--- Calendário Eletrônico TJCE ---)", content, re.DOTALL)
    if fortaleza_section_match:
        section_content = fortaleza_section_match.group(1).strip()
        lines = section_content.split('\n')
        current_year = 2025 # All these are in 2025
        for line in lines:
            line = line.strip()
            if not line.startswith('- '):
                continue
            
            month_match = re.match(r'^- ([A-ZÇ]+):\s*(\d{1,2}) \((.*)\)', line)
            if month_match:
                month_name = month_match.group(1).strip()
                day = int(month_match.group(2))
                description = month_match.group(3).strip()
                month_num = month_mapping.get(month_name.upper())
                if not month_num:
                    continue
                holidays.append({
                    'date': datetime(current_year, month_num, day).strftime('%Y-%m-%d'),
                    'description': description,
                    'type': 'Feriado',
                    'scope': 'Fortaleza'
                })

    # Process electronic calendar holidays (municipalities)
    electronic_calendar_section_match = re.search(r'--- Calendário Eletrônico TJCE ---\n(.*?)$', content, re.DOTALL)
    if electronic_calendar_section_match:
        section_content = electronic_calendar_section_match.group(1).strip()
        lines = section_content.split('\n')
        current_month_num = None
        current_year = 2025 # Default for this section, updated by month headers

        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            month_header_match = re.match(r'([A-Za-zÀ-ÖØ-öø-ÿ]+) (\d{4}):', line)
            if month_header_match:
                month_name = month_header_match.group(1).strip()
                current_year = int(month_header_match.group(2))
                current_month_num = month_mapping.get(month_name.upper())
                continue

            holiday_match = re.match(r'^- (\d{1,2}):\s*(.*?)\s*\((.*?)\)', line)
            if holiday_match and current_month_num is not None:
                day = int(holiday_match.group(1))
                description = holiday_match.group(2).strip()
                scope_info = holiday_match.group(3).strip()
                
                # Extract municipality from scope_info
                municipality = description # Default to description
                if 'Feriado Municipal em ' in scope_info:
                    municipality = scope_info.replace('Feriado Municipal em ', '').strip()
                elif 'Feriado Municipal' == scope_info:
                    # Municipality is already in the description
                    pass
                elif 'Recesso Forense' in description or 'Recesso Natalino' in description:
                    municipality = 'Nacional/Estadual'
                else:
                    # For cases like 'Aiuba, Aquiraz, Mombaça, Nova Russas e Uruoca'
                    municipality = scope_info

                # Handle multiple municipalities in one line
                if ',' in municipality or ' e ' in municipality:
                    municipalities = re.split(r',| e ', municipality)
                    for m in municipalities:
                        m = m.strip()
                        if m:
                            holidays.append({
                                'date': datetime(current_year, current_month_num, day).strftime('%Y-%m-%d'),
                                'description': description,
                                'type': 'Feriado Municipal',
                                'scope': m
                            })
                else:
                    holidays.append({
                        'date': datetime(current_year, current_month_num, day).strftime('%Y-%m-%d'),
                        'description': description,
                        'type': 'Feriado Municipal' if 'Feriado Municipal' in scope_info else ('Recesso' if 'Recesso' in description else 'Feriado'),
                        'scope': municipality
                    })

    return holidays

if __name__ == '__main__':
    parsed_data = parse_holiday_data('tjce_holidays_2025_2026.txt')
    # Remove duplicates and sort
    unique_holidays = []
    seen = set()
    for holiday in parsed_data:
        # Create a unique identifier for each holiday entry
        identifier = (holiday['date'], holiday['description'], holiday['scope'])
        if identifier not in seen:
            unique_holidays.append(holiday)
            seen.add(identifier)
    
    # Sort by date for easier readability
    unique_holidays.sort(key=lambda x: x['date'])

    with open('holidays.json', 'w', encoding='utf-8') as f:
        json.dump(unique_holidays, f, ensure_ascii=False, indent=4)
    print("Dados de feriados estruturados e salvos em holidays.json")


