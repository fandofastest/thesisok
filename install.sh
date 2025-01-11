#!/bin/bash

# Update dan upgrade sistem
sudo apt update -y

# Install Python dan pip
sudo apt install python3 python3-pip -y

# Buat virtual environment
sudo apt install python3-venv -y
python3 -m venv flask_env
source flask_env/bin/activate

# Install dependensi Python
pip install --upgrade pip
pip install flask numpy yfinance tensorflow scikit-learn

# Buat direktori proyek jika belum ada
PROJECT_DIR="/home/flask_crypto_app"
sudo mkdir -p $PROJECT_DIR
sudo chown $USER:$USER $PROJECT_DIR

# Salin file aplikasi ke direktori proyek
cp ./app.py $PROJECT_DIR
cp ./modeling_results.json $PROJECT_DIR
mkdir -p $PROJECT_DIR/models $PROJECT_DIR/plots

# Buat file systemd service untuk aplikasi Flask
SERVICE_FILE="/etc/systemd/system/flask_crypto_app.service"
echo "[Unit]
Description=Flask Crypto Prediction App
After=network.target

[Service]
User=$USER
WorkingDirectory=$PROJECT_DIR
ExecStart=/bin/bash -c 'source $PROJECT_DIR/flask_env/bin/activate && python3 $PROJECT_DIR/app.py'
Restart=always

[Install]
WantedBy=multi-user.target" | sudo tee $SERVICE_FILE

# Reload systemd dan aktifkan layanan Flask
sudo systemctl daemon-reload
sudo systemctl enable flask_crypto_app
sudo systemctl start flask_crypto_app

# Tampilkan status layanan
sudo systemctl status flask_crypto_app
