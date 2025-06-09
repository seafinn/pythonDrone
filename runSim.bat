@echo off
setlocal enabledelayedexpansion

set "PYTHON_SCRIPT=2dDroneModel.py"
set "OUTPUT_FILE=outputLog.txt"
set "DURATION_MINUTES=300"
set "INTERVAL_SECONDS=15"

:: Calculate end time
for /f "tokens=2 delims==" %%A in ('wmic os get localdatetime /value') do set "start_datetime=%%A"
set /a "end_time_minutes=%start_datetime:~8,2% * 60 + %start_datetime:~10,2% + DURATION_MINUTES"
set /a "end_hour=end_time_minutes / 60"
set /a "end_minute=end_time_minutes %% 60"

:loop
for /f "tokens=2 delims==" %%A in ('wmic os get localdatetime /value') do set "current_datetime=%%A"
set "current_hour=!current_datetime:~8,2!"
set "current_minute=!current_datetime:~10,2!"
if !current_hour!!current_minute! geq !end_hour!!end_minute! goto :end

:: Run Python and log to temp file (avoid locking)
echo [%DATE% %TIME%] Starting VPython >> %OUTPUT_FILE%
python %PYTHON_SCRIPT% > temp_log.txt 2>&1
type temp_log.txt >> %OUTPUT_FILE%
del temp_log.txt

:: Kill Python & browser to prevent hangs
taskkill /im python.exe /f >nul 2>&1
taskkill /im firefox.exe /f >nul 2>&1

timeout /t %INTERVAL_SECONDS% /nobreak >nul
goto :loop

:end
echo [%DATE% %TIME%] Done >> %OUTPUT_FILE%