@echo off
setlocal

if not exist jq.exe (
    echo jq.exe not found. Downloading jq for Windows...
    powershell -Command "Invoke-WebRequest -Uri https://github.com/stedolan/jq/releases/download/jq-1.6/jq-win64.exe -OutFile jq.exe"
    if exist jq.exe (
        echo jq.exe downloaded successfully.
    ) else (
        echo Error: jq.exe could not be downloaded. Please check your internet connection or download manually.
        exit /b 1
    )
)

if not exist package.json (
    echo package.json not found. Creating one...
    npm init -y
)

echo Modifying package.json to use ES modules...


jq ". + {\"type\": \"module\"}" package.json > temp.json && move /Y temp.json package.json

if %errorlevel% neq 0 (
    echo Error: Failed to modify package.json with jq.
    install.bat
)

echo Installing dependencies...
npm install node-fetch axios qs

if %errorlevel% neq 0 (
    echo Error: npm dependencies installation failed.
    exit /b 1
)

echo All set! ES modules configured and dependencies installed.


echo Installing Python dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Error: pip dependencies installation failed.
    exit /b 1
)

echo Running Python script...
python main.py

if %errorlevel% neq 0 (
    echo Error: Python script execution failed.
    exit /b 1
)

echo Python script executed successfully!

python main.py

endlocal
