import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import json
from calculate_deadline import calculate_judicial_deadline, load_holidays

class TJCEDeadlineCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Prazos Judiciais - TJCE")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Load holidays data
        try:
            self.holidays = load_holidays()
            self.comarcas = self.get_comarcas_list()
        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo de feriados não encontrado. Certifique-se de que o arquivo 'holidays.json' está presente.")
            self.holidays = []
            self.comarcas = []
        
        self.setup_ui()
    
    def get_comarcas_list(self):
        """Extract unique comarcas from holidays data"""
        comarcas = set()
        for holiday in self.holidays:
            if holiday['type'] == 'Feriado Municipal':
                comarcas.add(holiday['scope'])
        return sorted(list(comarcas))
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Calculadora de Prazos Judiciais", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        subtitle_label = ttk.Label(main_frame, text="Tribunal de Justiça do Estado do Ceará", 
                                  font=("Arial", 12))
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 30))
        
        # Start date input
        ttk.Label(main_frame, text="Data de Início:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.start_date_var = tk.StringVar(value=date.today().strftime('%d/%m/%Y'))
        self.start_date_entry = ttk.Entry(main_frame, textvariable=self.start_date_var, width=15)
        self.start_date_entry.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Days input
        ttk.Label(main_frame, text="Prazo (dias úteis):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.days_var = tk.StringVar()
        self.days_entry = ttk.Entry(main_frame, textvariable=self.days_var, width=15)
        self.days_entry.grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Comarca selection
        ttk.Label(main_frame, text="Comarca:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.comarca_var = tk.StringVar()
        self.comarca_combo = ttk.Combobox(main_frame, textvariable=self.comarca_var, 
                                         values=["Todas"] + self.comarcas, width=25)
        self.comarca_combo.set("Todas")
        self.comarca_combo.grid(row=4, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Calculate button
        calculate_btn = ttk.Button(main_frame, text="Calcular Prazo", 
                                  command=self.calculate_deadline)
        calculate_btn.grid(row=5, column=0, columnspan=2, pady=20)
        
        # Result frame
        result_frame = ttk.LabelFrame(main_frame, text="Resultado", padding="10")
        result_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.result_text = tk.Text(result_frame, height=8, width=60, wrap=tk.WORD)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Scrollbar for result text
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        # Instructions
        instructions = """
Instruções:
1. Insira a data de início no formato DD/MM/AAAA
2. Informe o prazo em dias úteis
3. Selecione a comarca (opcional - deixe "Todas" para considerar apenas feriados nacionais/estaduais)
4. Clique em "Calcular Prazo"

O sistema considera automaticamente:
- Sábados e domingos como não úteis
- Feriados nacionais e estaduais
- Feriados municipais (se comarca específica for selecionada)
- Recessos forenses
        """
        
        instructions_frame = ttk.LabelFrame(main_frame, text="Instruções", padding="10")
        instructions_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        instructions_label = ttk.Label(instructions_frame, text=instructions, justify=tk.LEFT)
        instructions_label.grid(row=0, column=0, sticky=tk.W)
    
    def calculate_deadline(self):
        try:
            # Validate inputs
            start_date_str = self.start_date_var.get().strip()
            days_str = self.days_var.get().strip()
            comarca = self.comarca_var.get().strip()
            
            if not start_date_str or not days_str:
                messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
                return
            
            # Parse start date
            try:
                start_date = datetime.strptime(start_date_str, '%d/%m/%Y').date()
                start_date_iso = start_date.strftime('%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Erro", "Data inválida. Use o formato DD/MM/AAAA.")
                return
            
            # Parse days
            try:
                num_days = int(days_str)
                if num_days <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Erro", "Prazo deve ser um número inteiro positivo.")
                return
            
            # Set comarca for calculation
            comarca_for_calc = None if comarca == "Todas" else comarca
            
            # Calculate deadline
            deadline_str = calculate_judicial_deadline(start_date_iso, num_days, comarca_for_calc)
            deadline_date = datetime.strptime(deadline_str, '%Y-%m-%d').date()
            
            # Format result
            result = f"RESULTADO DO CÁLCULO DE PRAZO\n"
            result += f"{'='*50}\n\n"
            result += f"Data de início: {start_date.strftime('%d/%m/%Y')} ({self.get_weekday_name(start_date)})\n"
            result += f"Prazo: {num_days} dias úteis\n"
            result += f"Comarca: {comarca}\n\n"
            result += f"Data de vencimento: {deadline_date.strftime('%d/%m/%Y')} ({self.get_weekday_name(deadline_date)})\n\n"
            
            # Show holidays that affect the calculation
            holidays_in_period = self.get_holidays_in_period(start_date, deadline_date, comarca_for_calc)
            if holidays_in_period:
                result += f"Feriados/Pontos Facultativos no período:\n"
                for holiday in holidays_in_period:
                    holiday_date = datetime.strptime(holiday['date'], '%Y-%m-%d').date()
                    result += f"- {holiday_date.strftime('%d/%m/%Y')}: {holiday['description']} ({holiday['scope']})\n"
            else:
                result += "Nenhum feriado ou ponto facultativo no período.\n"
            
            # Clear and display result
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, result)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no cálculo: {str(e)}")
    
    def get_weekday_name(self, date_obj):
        weekdays = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 
                   'Sexta-feira', 'Sábado', 'Domingo']
        return weekdays[date_obj.weekday()]
    
    def get_holidays_in_period(self, start_date, end_date, comarca):
        holidays_in_period = []
        for holiday in self.holidays:
            holiday_date = datetime.strptime(holiday['date'], '%Y-%m-%d').date()
            if start_date <= holiday_date <= end_date:
                if holiday['scope'] == 'Nacional/Estadual':
                    holidays_in_period.append(holiday)
                elif comarca and holiday['scope'].lower() == comarca.lower():
                    holidays_in_period.append(holiday)
        return sorted(holidays_in_period, key=lambda x: x['date'])

def main():
    root = tk.Tk()
    app = TJCEDeadlineCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()

