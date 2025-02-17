sudo apt-get install jq

if [ ! -f package.json ]; then
  echo "package.json not found. Creating one..."
  npm init -y
fi

echo "Modifying package.json to use ES modules..."

jq '. + {"type": "module"}' package.json > temp.json && mv temp.json package.json

echo "Installing dependencies..."
npm install node-fetch axios qs

echo "All set! ES modules configured and dependencies installed."

pip install -r requirements.txt
python main.py
