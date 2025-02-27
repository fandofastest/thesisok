# Cryptocurrency Price Prediction with LSTM & GRU

## Overview
This project focuses on predicting cryptocurrency prices using deep learning models (LSTM and GRU). The models are trained using historical price data and optimized with Bayesian Optimization and K-Fold Cross-Validation.

## Features
- Supports multiple deep learning architectures (LSTM, GRU, hybrid models).
- Fetches historical cryptocurrency data from Yahoo Finance.
- Scales data using MinMaxScaler.
- Uses Bayesian Optimization to fine-tune hyperparameters.
- Implements 5-Fold Cross-Validation for model evaluation.
- Saves the best-performing model and generates prediction plots.
- Provides an API for model inference using `app.py`.

## Installation
Ensure you have Python installed, then install the required dependencies:

```bash
pip install -r requirements.txt
```

## Dependencies
- `numpy`
- `pandas`
- `tensorflow`
- `scikit-learn`
- `matplotlib`
- `bayesian-optimization`
- `yfinance`
- `flask` (for API)

## Usage
### Training the Model
Run the script to train models and evaluate performance:

```bash
Google Colab
```

This script will:
1. Download historical cryptocurrency data.
2. Train multiple deep learning models.
3. Optimize hyperparameters using Bayesian Optimization.
4. Perform K-Fold Cross-Validation.
5. Save the best model in the `models` directory.
6. Generate and save evaluation plots in the `plots` directory.

### Running the API
To serve the trained model via an API, run:

```bash
python app.py
```

This will start a Flask-based API that allows users to get predictions for cryptocurrency prices.

## Results
- The trained models are saved in the `models/` directory.
- Evaluation results are stored in `evaluation_results_kfold.json`.
- Performance plots are saved in the `plots/` directory.

## File Structure
```
.
├── models/                  # Saved trained models
├── plots/                   # Prediction plots
├── app.py                   # API for model inference
├── LSTM_GRU.ipynb           # Jupyter Notebook for training
├── evaluation_results_kfold.json  # Evaluation results
├── requirements.txt         # Required dependencies
└── README.md                # Project documentation
```

## Author
[Rifando Panggabean](https://github.com/fandofastest)

## License
This project is open-source under the MIT License.

