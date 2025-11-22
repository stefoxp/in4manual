@echo off
setlocal ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION

rem ========================================
rem Setup Ambiente CSV Control (Batch)
rem ========================================
echo ========================================
echo Setup Ambiente CSV Control
echo ========================================
echo.

rem 1. Individua il comando Python di sistema
set "SYS_PYTHON="
set "PY_VERSION="

for %%C in ("py -3" "py" "python") do (
    call :DetectPython %%C
    if defined SYS_PYTHON goto :PythonFound
)

echo [ERRORE] Python non trovato. Installa Python 3.8 o superiore.
exit /b 1

:PythonFound
echo [OK] Python trovato: !PY_VERSION!

rem 2. Crea ambiente virtuale se mancante
if not exist venv (
    echo.
    echo [INFO] Creazione ambiente virtuale...
    %SYS_PYTHON% -m venv venv
    if errorlevel 1 (
        echo [ERRORE] Creazione ambiente virtuale fallita.
        exit /b 1
    )
    echo [OK] Ambiente virtuale creato.
) else (
    echo.
    echo [INFO] Ambiente virtuale gia' presente.
)

set "VENV_PY=venv\Scripts\python.exe"
if not exist "%VENV_PY%" (
    echo [ERRORE] Impossibile trovare %VENV_PY%. Verifica la creazione del venv.
    exit /b 1
)

echo.
echo [INFO] Aggiornamento pip...
call "%VENV_PY%" -m pip install --upgrade pip >nul
if errorlevel 1 (
    echo [ERRORE] Aggiornamento pip fallito.
    exit /b 1
)
echo [OK] pip aggiornato.

echo.
echo [INFO] Installazione dipendenze da requirements.txt...
if exist requirements.txt (
    call "%VENV_PY%" -m pip install -r requirements.txt >nul
    if errorlevel 1 (
        echo [ERRORE] Installazione dipendenze fallita.
        exit /b 1
    )
    echo [OK] Dipendenze installate.
) else (
    echo [ERRORE] File requirements.txt non trovato.
    exit /b 1
)

echo.
echo [INFO] Verifica pytest...
call "%VENV_PY%" -m pytest --version >nul
if errorlevel 1 (
    echo [ERRORE] pytest non installato correttamente.
) else (
    echo [OK] pytest disponibile.
)

echo.
echo ========================================
echo Setup completato!
echo ========================================
echo.
echo Per attivare l'ambiente eseguire: call venv\Scripts\activate.bat
echo Per disattivare l'ambiente:    deactivate

echo.
exit /b 0

:DetectPython
set "CAND=%~1"
%CAND% --version >nul 2>&1
if errorlevel 1 goto :EOF
for /f "delims=" %%V in ('%CAND% --version 2^>^&1') do (
    set "SYS_PYTHON=%CAND%"
    set "PY_VERSION=%%V"
)
goto :EOF
