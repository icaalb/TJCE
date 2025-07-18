@echo off
echo Instalando Calculadora de Prazos Judiciais - TJCE
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python não está instalado ou não está no PATH.
    echo Por favor, instale o Python 3.7 ou superior de https://python.org
    echo Certifique-se de marcar "Add Python to PATH" durante a instalação.
    pause
    exit /b 1
)

echo Python encontrado. Instalando dependências...
pip install flask

echo.
echo Instalação concluída!
echo.
echo Para executar o aplicativo:
echo 1. Execute: python tjce_deadline_calculator_web.py
echo 2. Abra seu navegador e acesse: http://localhost:8080
echo.
pause

