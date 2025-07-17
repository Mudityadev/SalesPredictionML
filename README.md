# SalesPrediction Desktop App

## Overview

SalesPrediction is a desktop GUI application built with **Tkinter** in Python that predicts the **total combined sales** for a product across three stores using a trained **XGBoost regression model**. The model is trained on historical sales data and saved as `xgb_sales_model.pkl`, with the expected input columns stored in `model_columns.pkl`.

## Features

- User-friendly desktop interface for sales prediction
- Input fields for product and environment details:
  - Product Calorie (float)
  - Promotion Applied (checkbox)
  - Day (dropdown: Monday to Sunday)
  - StoreID (dropdown: S001, S002, S003)
  - Product Name (dropdown: VBurger)
  - Weather (dropdown: cold, hot, humid, rainy, very hot)
  - Inflation % (float)
  - Unemployment % (float)
- One-hot encoding for categorical variables
- Handles missing columns by filling with zero
- Displays predicted total sales in a popup

## Files

- `app.py` - Main Tkinter GUI application
- `xgb_sales_model.pkl` - Trained XGBoost regression model
- `model_columns.pkl` - List of feature column names used by the model
- `requirements.txt` - Python dependencies
- `artificial_sales.csv` - Example sales data (optional)

## Getting Started

### Prerequisites

- Python 3.7+
- The following Python packages (see `requirements.txt`):
  - xgboost
  - joblib
  - pandas
  - tkinter (usually included with Python)

### Installation

1. Clone or download this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure `xgb_sales_model.pkl` and `model_columns.pkl` are present in the project directory.

### Running the App

Run the following command in your terminal:

```bash
python app.py
```

The Tkinter GUI will open. Enter the required details and click **Predict** to see the predicted total sales.

## Packaging as an Executable (Optional)

To create a standalone `.exe` file (Windows):

```bash
pyinstaller --onefile app.py
```

The executable will be created in the `dist/` folder.

## Extending the App

- Add more input fields (e.g., "specials", "mods")
- Add charts or historical prediction graphs

## License

This project is for educational/demo purposes. Please adapt as needed for your use case. 