#!/bin/bash

if [ -f "/etc/debian_version" ]; then
    PKG_MANAGER="apt-get"
    PYTHON_CMD="python3"
    REQUIRED_PACKAGES="jq nodejs npm python3-pip"
elif [ -d "/data/data/com.termux/files/usr" ]; then
    PKG_MANAGER="pkg"
    PYTHON_CMD="python"
    REQUIRED_PACKAGES="jq nodejs npm python"
else
    echo "Unsupported system." >&2
    exit 1
fi

"$PKG_MANAGER" update -y || { echo "Error updating packages." >&2; exit 1; }
"$PKG_MANAGER" install -y $REQUIRED_PACKAGES || { echo "Error installing required packages." >&2; exit 1; }

[ ! -f package.json ] && npm init -y || true
jq '. + {"type": "module"}' package.json > temp.json && mv temp.json package.json || { echo "Error modifying package.json." >&2; exit 1; }

npm install node-fetch axios qs || { echo "Error installing npm dependencies." >&2; exit 1; }

if [ -f requirements.txt ]; then
    pip install -r requirements.txt || { echo "Error installing Python dependencies." >&2; exit 1; }
fi

"$PYTHON_CMD" main.py || { echo "Error executing main.py." >&2; exit 1; }

echo "Script completed."
