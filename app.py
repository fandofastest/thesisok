from flask import Flask, request, jsonify, send_from_directory
import os
import numpy as np
import json
import yfinance as yf
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta
from flask_cors import CORS  # Import CORS

# Inisialisasi Flask
app = Flask(__name__)
CORS(app)  # Mengizinkan semua origin untuk mengakses aplikasi

# Path ke file JSON hasil modeling
JSON_FILE = './modeling_results.json'
MODEL_PATH = './models'
PLOT_PATH = './plots'
CRYPTO_LIST = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'SOL-USD', 'XRP-USD']

# Fungsi untuk memuat model
def load_model(crypto, model_id):
    model_file = f"{MODEL_PATH}/{crypto}_model_{model_id}_best.h5"
    if not os.path.exists(model_file):
        raise FileNotFoundError(f"Model {model_file} tidak ditemukan.")
    return tf.keras.models.load_model(model_file)

# Fungsi untuk mendapatkan data historis 120 hari terakhir dari Yahoo Finance
def get_last_120_days_data(crypto):
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=120)
        data = yf.download(crypto, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))

        if data.empty:
            raise ValueError(f"Tidak ada data yang ditemukan untuk {crypto}.")

        close_prices = data['Close'].values

        if len(close_prices) < 120:
            print(f"Data tidak mencukupi untuk {crypto}, hanya {len(close_prices)} hari yang tersedia. Data akan diisi ulang dengan padding nol.")
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = scaler.fit_transform(close_prices.reshape(-1, 1))

            # Padding dengan nol di awal untuk mencapai 120 hari
            padded_data = np.zeros((120, 1))  # Padding nol
            padded_data[-len(scaled_data):] = scaled_data  # Sisipkan data di akhir

            return padded_data.reshape(1, -1, 1), scaler
        else:
            # Normalisasi data
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = scaler.fit_transform(close_prices.reshape(-1, 1))
            return scaled_data[-120:].reshape(1, -1, 1), scaler

    except Exception as e:
        raise ValueError(f"Gagal mengambil data dari Yahoo Finance: {str(e)}")

# Fungsi untuk mendapatkan detail model dari JSON
def get_model_details(crypto, model_id):
    try:
        # Baca file JSON
        with open(JSON_FILE, 'r') as f:
            data = json.load(f)

        # Ambil data model terkait
        model_name = f"{crypto}_model_{model_id}"
        if model_name not in data:
            raise ValueError(f"Detail untuk {model_name} tidak ditemukan.")

        model_info = data[model_name]
        best_r2_score = model_info.get('best_r2_score')
        best_fold = None
        for fold_result in model_info.get('fold_results', []):
            if fold_result.get('R²') == best_r2_score:
                best_fold = fold_result
                break

        return {
            'structure': model_info.get('structure', []),
            'best_fold_result': best_fold
        }
    except FileNotFoundError:
        raise FileNotFoundError("File modeling_results.json tidak ditemukan.")
    except Exception as e:
        raise ValueError(f"Terjadi kesalahan saat membaca detail model: {str(e)}")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Ambil input dari request
        data = request.json
        crypto = data.get('crypto')
        model_id = data.get('model_id')

        # Validasi input
        if crypto not in CRYPTO_LIST:
            return jsonify({'error': f"Crypto {crypto} tidak valid. Pilih dari {CRYPTO_LIST}."}), 400
        if not isinstance(model_id, int) or not (1 <= model_id <= 6):
            return jsonify({'error': "Model ID harus berupa integer antara 1 dan 6."}), 400

        # Muat model
        model = load_model(crypto, model_id)

        # Ambil data 120 hari terakhir dari Yahoo Finance
        input_data, scaler = get_last_120_days_data(crypto)

        # Prediksi harga hari ini
        prediction = model.predict(input_data)

        # Denormalisasi prediksi
        predicted_price = scaler.inverse_transform(prediction)[0][0]

        # Dapatkan detail model
        model_details = get_model_details(crypto, model_id)

        # Buat link ke plot model, dengan menggunakan root URL dari server
        plot_file = f"{crypto}_model_{model_id}_plot.png"
        if not os.path.exists(os.path.join(PLOT_PATH, plot_file)):
            plot_link = None
        else:
            plot_link = f"{request.url_root}plots/{plot_file}"  # Menggunakan route /plots/ di server saat ini

        # Kembalikan respons JSON
        response = {
            'crypto': crypto,
            'model_id': model_id,
            'predicted_price': float(predicted_price),
            'plot_link': plot_link,
            'model_details': model_details
        }
        return jsonify(response), 200

    except FileNotFoundError as e:
        return jsonify({'error': str(e)}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Terjadi kesalahan: {str(e)}"}), 500

# Route untuk melayani file plot dari folder ./plots
@app.route('/plots/<filename>')
def serve_plot(filename):
    # Menyajikan file gambar dari folder ./plots
    return send_from_directory(PLOT_PATH, filename)

if __name__ == '__main__':
    # Pastikan host dan port sesuai kebutuhan Anda
    app.run(host='0.0.0.0', port=5000)
