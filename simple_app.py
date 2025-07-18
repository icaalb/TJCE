from flask import Flask, render_template_string, request, jsonify
from datetime import datetime, date
import json
from calculate_deadline import calculate_judicial_deadline, load_holidays

app = Flask(__name__)

# Load holidays data
try:
    holidays = load_holidays()
    comarcas = sorted(list(set([h['scope'] for h in holidays if h['type'] == 'Feriado Municipal'])))
except:
    holidays = []
    comarcas = []

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Calculadora de Prazos Judiciais - TJCE</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .header { background: #1e3c72; color: white; padding: 20px; text-align: center; margin-bottom: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, select { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        button { background: #1e3c72; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        .result { margin-top: 20px; padding: 15px; background: #f8f9fa; border-left: 5px solid #1e3c72; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Calculadora de Prazos Judiciais</h1>
        <p>Tribunal de Justiça do Estado do Ceará</p>
    </div>
    
    <form id="form">
        <div class="form-group">
            <label>Data de Início:</label>
            <input type="date" id="start_date" required>
        </div>
        <div class="form-group">
            <label>Prazo (dias úteis):</label>
            <input type="number" id="num_days" min="1" required>
        </div>
        <div class="form-group">
            <label>Comarca:</label>
            <select id="comarca">
                <option value="Todas">Todas</option>
            </select>
        </div>
        <button type="submit">Calcular Prazo</button>
    </form>
    
    <div id="result" class="result" style="display:none;"></div>
    
    <script>
        document.getElementById('form').onsubmit = async function(e) {
            e.preventDefault();
            const data = {
                start_date: document.getElementById('start_date').value,
                num_days: document.getElementById('num_days').value,
                comarca: document.getElementById('comarca').value
            };
            
            try {
                const response = await fetch('/calculate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                const result = await response.json();
                
                if (result.success) {
                    document.getElementById('result').innerHTML = 
                        '<h3>Resultado:</h3>' +
                        '<p><strong>Data de vencimento:</strong> ' + result.deadline_date + ' (' + result.deadline_weekday + ')</p>' +
                        '<p><strong>Prazo:</strong> ' + result.num_days + ' dias úteis</p>' +
                        '<p><strong>Comarca:</strong> ' + result.comarca + '</p>';
                    document.getElementById('result').style.display = 'block';
                } else {
                    document.getElementById('result').innerHTML = '<p style="color:red;">Erro: ' + result.error + '</p>';
                    document.getElementById('result').style.display = 'block';
                }
            } catch (error) {
                document.getElementById('result').innerHTML = '<p style="color:red;">Erro de conexão</p>';
                document.getElementById('result').style.display = 'block';
            }
        };
        
        // Set today's date
        document.getElementById('start_date').value = new Date().toISOString().split('T')[0];
    </script>
</body>
</html>
    '''

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        start_date_str = data.get('start_date')
        num_days = int(data.get('num_days'))
        comarca = data.get('comarca')
        
        if comarca == 'Todas':
            comarca = None
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        deadline_str = calculate_judicial_deadline(start_date_str, num_days, comarca)
        deadline_date = datetime.strptime(deadline_str, '%Y-%m-%d').date()
        
        weekdays = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
        
        return jsonify({
            'success': True,
            'deadline_date': deadline_date.strftime('%d/%m/%Y'),
            'deadline_weekday': weekdays[deadline_date.weekday()],
            'num_days': num_days,
            'comarca': comarca or 'Todas'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
