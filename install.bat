@echo off
setlocal enableDelayedExpansion

:: --- Configuration ---
set "JQ_DOWNLOAD_URL=https://github.com/stedolan/jq/releases/download/jq-1.6/jq-win64.exe"
set "JQ_EXE_NAME=jq.exe"
set "NPM_DEPS=node-fetch axios qs"
set "PYTHON_REQ_FILE=requirements.txt"
set "MAIN_PYTHON_SCRIPT=main.py"

:: --- Functions ---
:: Function to check last command's error level
:CheckError
if %errorlevel% neq 0 (
    echo ERROR: %~1
    exit /b %errorlevel%
)
goto :eof

:: --- Main Script ---

echo Checking for %JQ_EXE_NAME%...
if not exist "%JQ_EXE_NAME%" (
    echo %JQ_EXE_NAME% not found. Downloading for Windows...
    powershell -Command "Invoke-WebRequest -Uri '%JQ_DOWNLOAD_URL%' -OutFile '%JQ_EXE_NAME%'"
    call :CheckError "Failed to download %JQ_EXE_NAME%."
    echo %JQ_EXE_NAME% downloaded successfully.
)

echo Checking for package.json...
if not exist package.json (
    echo package.json not found. Creating one with 'npm init -y'...
    npm init -y
    call :CheckError "Failed to initialize package.json."
)

echo Modifying package.json to use ES modules...
jq ". + {\"type\": \"module\"}" package.json > temp.json && move /Y temp.json package.json
call :CheckError "Failed to modify package.json with jq. Ensure jq.exe is in PATH or current directory, and package.json is valid JSON."

echo Installing Node.js dependencies (%NPM_DEPS%)...
npm install %NPM_DEPS%
call :CheckError "Failed to install npm dependencies."

echo Installing Python dependencies from %PYTHON_REQ_FILE%...
if exist "%PYTHON_REQ_FILE%" (
    pip install -r "%PYTHON_REQ_FILE%"
    call :CheckError "Failed to install pip dependencies from %PYTHON_REQ_FILE%."
) else (
    echo Warning: %PYTHON_REQ_FILE% not found. Skipping Python dependency installation.
)

echo Running Python script: %MAIN_PYTHON_SCRIPT%...
if not exist "%MAIN_PYTHON_SCRIPT%" (
    echo ERROR: %MAIN_PYTHON_SCRIPT% not found.
    exit /b 1
)
python "%MAIN_PYTHON_SCRIPT%"
call :CheckError "Python script execution failed."

echo All setup and scripts completed successfully!

endlocal
