#!/bin/bash

# Detect system (Debian or Termux)
if [ -f "/etc/debian_version" ]; then
    PKG_MANAGER="apt-get"
elif [ -d "/data/data/com.termux/files/usr" ]; then
    PKG_MANAGER="pkg"
else
    echo "Unsupported system." >&2
    exit 1
fi

# Update packages and install dependencies
$PKG_MANAGER update -y && $PKG_MANAGER install -y jq nodejs npm python3-pip

# Ensure package.json exists
if [ ! -f package.json ]; then
    echo "package.json not found. Creating one..."
    npm init -y
fi

# Modify package.json to use ES modules
echo "Modifying package.json to use ES modules..."
jq '. + {"type": "module"}' package.json > temp.json && mv temp.json package.json

# Install Node.js dependencies
echo "Installing dependencies..."
npm install node-fetch axios qs

# Install Python dependencies
pip install -r requirements.txt

# Run the Python script
python3 main.py
