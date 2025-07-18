# Calculadora de Prazos Judiciais - TJCE

## Descrição

Este aplicativo foi desenvolvido para calcular prazos judiciais na Justiça Estadual do Ceará, considerando automaticamente:

- Dias úteis (excluindo sábados e domingos)
- Feriados nacionais e estaduais
- Feriados municipais específicos de cada comarca
- Recessos forenses
- Pontos facultativos

## Características

- Interface web moderna e responsiva
- Cálculo automático baseado no calendário oficial do TJCE 2025-2026
- Suporte a todas as comarcas do Ceará
- Exibição detalhada dos feriados que afetam o prazo
- Funciona em qualquer sistema operacional com Python

## Requisitos do Sistema

- Python 3.7 ou superior
- Navegador web moderno (Chrome, Firefox, Edge, Safari)
- Conexão com a internet (apenas para download inicial)

## Instalação

### Windows

1. **Instalar Python:**
   - Baixe o Python em https://python.org
   - Durante a instalação, marque "Add Python to PATH"

2. **Instalar o aplicativo:**
   - Extraia todos os arquivos em uma pasta
   - Execute o arquivo `install.bat`
   - Aguarde a instalação das dependências

### Linux/Mac

1. **Verificar Python:**
   ```bash
   python3 --version
   ```

2. **Instalar dependências:**
   ```bash
   pip3 install flask
   ```

## Como Usar

### Método 1: Interface Web (Recomendado)

1. **Executar o aplicativo:**
   ```bash
   python tjce_deadline_calculator_web.py
   ```
   
2. **Acessar no navegador:**
   - Abra seu navegador
   - Acesse: http://localhost:8080

3. **Usar a calculadora:**
   - Selecione a data de início
   - Informe o prazo em dias úteis
   - Escolha a comarca (opcional)
   - Clique em "Calcular Prazo"

### Método 2: Interface Desktop (Tkinter)

1. **Executar o aplicativo:**
   ```bash
   python tjce_deadline_calculator.py
   ```

2. **Usar a interface:**
   - Preencha os campos solicitados
   - Clique em "Calcular Prazo"

## Estrutura dos Arquivos

```
TJCE_Calculadora_Prazos/
├── tjce_deadline_calculator_web.py    # Aplicativo web principal
├── tjce_deadline_calculator.py        # Aplicativo desktop (Tkinter)
├── calculate_deadline.py              # Lógica de cálculo de prazos
├── holidays.json                      # Base de dados de feriados
├── parse_holidays.py                  # Script para processar feriados
├── simple_app.py                      # Versão simplificada
├── templates/
│   └── index.html                     # Template da interface web
├── install.bat                        # Script de instalação Windows
└── README.md                          # Este arquivo
```

## Funcionalidades Detalhadas

### Cálculo de Prazos

O sistema calcula prazos judiciais seguindo as regras:

1. **Dias úteis:** Segunda a sexta-feira
2. **Exclusões automáticas:**
   - Sábados e domingos
   - Feriados nacionais (ex: Tiradentes, Independência)
   - Feriados estaduais (ex: Data Magna do Ceará)
   - Feriados municipais (quando comarca específica for selecionada)
   - Recessos forenses (ex: Recesso Natalino)
   - Pontos facultativos

### Base de Dados de Feriados

O aplicativo utiliza dados oficiais do TJCE para 2025-2026, incluindo:

- **Feriados Nacionais/Estaduais:** Aplicam-se a todas as comarcas
- **Feriados Municipais:** Específicos de cada município/comarca
- **Recessos:** Períodos em que a Justiça não funciona
- **Pontos Facultativos:** Dias de funcionamento opcional

### Comarcas Suportadas

O sistema suporta todas as comarcas do Ceará, incluindo:
- Fortaleza
- Sobral
- Juazeiro do Norte
- Caucaia
- Maracanaú
- E todas as demais comarcas do estado

## Exemplos de Uso

### Exemplo 1: Prazo Nacional
- **Data início:** 17/07/2025 (quinta-feira)
- **Prazo:** 5 dias úteis
- **Comarca:** Todas
- **Resultado:** 24/07/2025 (quinta-feira)

### Exemplo 2: Prazo com Feriado Municipal
- **Data início:** 14/08/2025 (quinta-feira)
- **Prazo:** 3 dias úteis
- **Comarca:** Fortaleza
- **Resultado:** 18/08/2025 (segunda-feira)
- **Observação:** Considera o feriado de Nossa Senhora da Assunção (15/08)

### Exemplo 3: Prazo com Recesso
- **Data início:** 18/12/2025 (quinta-feira)
- **Prazo:** 5 dias úteis
- **Comarca:** Todas
- **Resultado:** 07/01/2026 (quarta-feira)
- **Observação:** Considera o Recesso Natalino (20/12/2025 a 06/01/2026)

## Solução de Problemas

### Erro: "Python não encontrado"
- Certifique-se de que o Python está instalado
- Verifique se o Python está no PATH do sistema
- Reinstale o Python marcando "Add Python to PATH"

### Erro: "Módulo flask não encontrado"
- Execute: `pip install flask`
- No Windows, use: `python -m pip install flask`

### Erro: "Arquivo holidays.json não encontrado"
- Certifique-se de que todos os arquivos estão na mesma pasta
- Verifique se o arquivo holidays.json não foi corrompido

### Aplicativo não abre no navegador
- Verifique se o aplicativo está rodando (deve mostrar mensagens no terminal)
- Tente acessar: http://127.0.0.1:8080
- Verifique se a porta 8080 não está sendo usada por outro programa

## Atualizações

Para atualizar a base de feriados:

1. Obtenha o novo calendário do TJCE
2. Atualize o arquivo `tjce_holidays_2025_2026.txt`
3. Execute: `python parse_holidays.py`
4. O arquivo `holidays.json` será atualizado automaticamente

## Suporte Técnico

Para problemas técnicos ou dúvidas:

1. Verifique a seção "Solução de Problemas"
2. Certifique-se de que todos os arquivos estão presentes
3. Verifique se as dependências estão instaladas corretamente

## Licença

Este software foi desenvolvido para uso interno e educacional. Baseado em dados públicos do Tribunal de Justiça do Estado do Ceará.

## Histórico de Versões

### v1.0 (Julho 2025)
- Versão inicial
- Suporte a calendário TJCE 2025-2026
- Interface web e desktop
- Cálculo automático de prazos
- Suporte a todas as comarcas do Ceará

---

**Desenvolvido para o Tribunal de Justiça do Estado do Ceará**  
**Data:** Julho 2025

