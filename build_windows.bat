@echo off
REM Builds TicketManager.exe on Windows.
REM Run this from a Command Prompt / PowerShell inside the project folder.

setlocal

echo Creating virtual environment (.venv) if it doesn't exist...
if not exist ".venv" (
    python -m venv .venv
)

call .venv\Scripts\activate.bat

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-build.txt

echo Building TicketManager.exe...
pyinstaller ticket_manager.spec --noconfirm

echo.
echo Done. Your exe is at: dist\TicketManager.exe
pause
