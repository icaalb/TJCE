from flask import Flask, render_template, request, jsonify
from datetime import datetime, date
import json
from calculate_deadline import calculate_judicial_deadline, load_holidays

app = Flask(__name__)

# Load holidays data
try:
    holidays = load_holidays()
    comarcas = sorted(list(set([h['scope'] for h in holidays if h['type'] == 'Feriado Municipal'])))
except FileNotFoundError:
    holidays = []
    comarcas = []

def get_weekday_name(date_obj):
    weekdays = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 
               'Sexta-feira', 'Sábado', 'Domingo']
    return weekdays[date_obj.weekday()]

def get_holidays_in_period(start_date, end_date, comarca):
    holidays_in_period = []
    for holiday in holidays:
        holiday_date = datetime.strptime(holiday['date'], '%Y-%m-%d').date()
        if start_date <= holiday_date <= end_date:
            if holiday['scope'] == 'Nacional/Estadual':
                holidays_in_period.append(holiday)
            elif comarca and holiday['scope'].lower() == comarca.lower():
                holidays_in_period.append(holiday)
    return sorted(holidays_in_period, key=lambda x: x['date'])

@app.route('/')
def index():
    return render_template('index.html', comarcas=comarcas, today=date.today().strftime('%Y-%m-%d'))

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        start_date_str = data.get('start_date')
        num_days = int(data.get('num_days'))
        comarca = data.get('comarca')
        
        if comarca == 'Todas':
            comarca = None
        
        # Parse start date
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        
        # Calculate deadline
        deadline_str = calculate_judicial_deadline(start_date_str, num_days, comarca)
        deadline_date = datetime.strptime(deadline_str, '%Y-%m-%d').date()
        
        # Get holidays in period
        holidays_in_period = get_holidays_in_period(start_date, deadline_date, comarca)
        
        result = {
            'success': True,
            'start_date': start_date.strftime('%d/%m/%Y'),
            'start_weekday': get_weekday_name(start_date),
            'num_days': num_days,
            'comarca': comarca or 'Todas',
            'deadline_date': deadline_date.strftime('%d/%m/%Y'),
            'deadline_weekday': get_weekday_name(deadline_date),
            'holidays': [
                {
                    'date': datetime.strptime(h['date'], '%Y-%m-%d').strftime('%d/%m/%Y'),
                    'description': h['description'],
                    'scope': h['scope']
                } for h in holidays_in_period
            ]
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

