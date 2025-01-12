#!/bin/bash

# Update dan upgrade sistem
sudo apt update -y

# Install Python dan pip
sudo apt install python3 python3-pip python3-venv -y

# Install dependensi lainnya
sudo apt install python3-dev libpq-dev -y

# Buat virtual environment untuk aplikasi
python3 -m venv flask_env
source flask_env/bin/activate

# Upgrade pip dan install dependensi Python
pip install --upgrade pip
pip install flask numpy yfinance tensorflow scikit-learn
pip install flask-cors


# Buat direktori proyek jika belum ada
PROJECT_DIR="/home/$USER/flask_crypto_app"
mkdir -p $PROJECT_DIR
sudo chown -R $USER:$USER $PROJECT_DIR

# Salin file aplikasi Flask (app.py) dan modeling_results.json ke direktori proyek
echo "Copying Flask app files..."
cp ./app.py $PROJECT_DIR/
cp ./modeling_results.json $PROJECT_DIR/

# Salin folder models dan plots ke dalam direktori proyek
echo "Copying models and plots folders..."
cp -r ./models $PROJECT_DIR/
cp -r ./plots $PROJECT_DIR/

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
