@echo off
REM Builds TicketManager.exe and, if Inno Setup is installed, the installer.
REM Run this from a Command Prompt / PowerShell inside the project folder.

setlocal

REM ---- Find Python (the Microsoft Store shortcut does not count) ----
set "PY="
py -3 --version >nul 2>&1
if not errorlevel 1 set "PY=py -3"
if "%PY%"=="" (
    python --version >nul 2>&1
    if not errorlevel 1 set "PY=python"
)
if "%PY%"=="" goto :nopython

echo Using Python: %PY%
echo Creating virtual environment (.venv) if it doesn't exist...
if not exist ".venv\Scripts\activate.bat" (
    %PY% -m venv .venv
)
if not exist ".venv\Scripts\activate.bat" goto :novenv

call .venv\Scripts\activate.bat

echo Installing dependencies...
python -m pip install --upgrade pip
if errorlevel 1 goto :failed
python -m pip install -r requirements.txt
if errorlevel 1 goto :failed
python -m pip install -r requirements-build.txt
if errorlevel 1 goto :failed

echo Building TicketManager.exe...
python -m PyInstaller ticket_manager.spec --noconfirm
if errorlevel 1 goto :failed

echo.
echo Exe ready: dist\TicketManager.exe
echo.

REM ---- Optional: build the installer with Inno Setup 6 ----
set "ISCC="
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles%\Inno Setup 6\ISCC.exe"
if exist "%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe" set "ISCC=%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe"

if "%ISCC%"=="" goto :noinno

echo Building installer...
"%ISCC%" installer\TicketManager.iss
if errorlevel 1 goto :failed
echo.
echo Done. Installer is in the installer_output folder.
goto :end

:nopython
echo.
echo Python was not found.
echo 1. Download Python 3.12 (64-bit) from https://www.python.org/downloads/
echo 2. In the installer, tick "Add python.exe to PATH" before clicking Install.
echo 3. Close this window, open a new Command Prompt, and run this file again.
goto :end

:novenv
echo.
echo Could not create the virtual environment (.venv).
echo Make sure Python was installed with the "venv" option, then try again.
goto :end

:noinno
echo Inno Setup 6 was not found, so the installer was not built.
echo Install it from https://jrsoftware.org/isdl.php and run this file again.
goto :end

:failed
echo.
echo Build failed. See the messages above.

:end
pause
