#!/bin/bash

if [ "$(id -u)" -ne 0 ]; then
    echo "Please run this script as root (sudo)." >&2
    exit 1
fi

if [ -f "/etc/debian_version" ]; then
    PKG_MANAGER="apt-get"
elif [ -d "/data/data/com.termux/files/usr" ]; then
    PKG_MANAGER="pkg"
else
    echo "Unsupported system." >&2
    exit 1
fi

$PKG_MANAGER update -y && $PKG_MANAGER install -y jq nodejs npm python3-pip

if [ ! -f package.json ]; then
    echo "package.json not found. Creating one..."
    npm init -y
fi

echo "Modifying package.json to use ES modules..."
jq '. + {"type": "module"}' package.json > temp.json && mv temp.json package.json

echo "Installing dependencies..."
npm install node-fetch axios qs

pip install -r requirements.txt
python3 main.py
