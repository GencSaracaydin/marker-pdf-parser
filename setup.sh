#!/bin/bash
set -e

sudo apt update
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs python3.11-venv

mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=$HOME/.npm-global/bin:$PATH' >> ~/.profile
source ~/.profile

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

echo "[✔] Setup complete. Now you can run: ./parse.sh <PDF_FOLDER>"

