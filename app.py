import tkinter as tk
from tkinter import ttk, messagebox
import joblib
import pandas as pd
import os

# Placeholder for model and columns file paths
MODEL_PATH = 'xgb_sales_model.pkl'
COLUMNS_PATH = 'model_columns.pkl'

class SalesPredictionApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Sales Prediction App')
        self.create_widgets()

    def create_widgets(self):
        # Product Calorie
        tk.Label(self.root, text='Product Calorie:').grid(row=0, column=0, sticky='e')
        self.calorie_var = tk.DoubleVar()
        tk.Entry(self.root, textvariable=self.calorie_var).grid(row=0, column=1)

        # Promotion Applied
        self.promo_var = tk.IntVar()
        tk.Checkbutton(self.root, text='Promotion Applied', variable=self.promo_var).grid(row=1, column=1, sticky='w')

        # Day Dropdown
        tk.Label(self.root, text='Day:').grid(row=2, column=0, sticky='e')
        self.day_var = tk.StringVar()
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        ttk.Combobox(self.root, textvariable=self.day_var, values=days, state='readonly').grid(row=2, column=1)

        # StoreID Dropdown
        tk.Label(self.root, text='StoreID:').grid(row=3, column=0, sticky='e')
        self.store_var = tk.StringVar()
        stores = ['S001', 'S002', 'S003']
        ttk.Combobox(self.root, textvariable=self.store_var, values=stores, state='readonly').grid(row=3, column=1)

        # Product Name Dropdown
        tk.Label(self.root, text='Product Name:').grid(row=4, column=0, sticky='e')
        self.product_var = tk.StringVar()
        products = ['VBurger']
        ttk.Combobox(self.root, textvariable=self.product_var, values=products, state='readonly').grid(row=4, column=1)

        # Weather Dropdown
        tk.Label(self.root, text='Weather:').grid(row=5, column=0, sticky='e')
        self.weather_var = tk.StringVar()
        weathers = ['cold', 'hot', 'humid', 'rainy', 'very hot']
        ttk.Combobox(self.root, textvariable=self.weather_var, values=weathers, state='readonly').grid(row=5, column=1)

        # Inflation %
        tk.Label(self.root, text='Inflation %:').grid(row=6, column=0, sticky='e')
        self.inflation_var = tk.DoubleVar()
        tk.Entry(self.root, textvariable=self.inflation_var).grid(row=6, column=1)

        # Unemployment %
        tk.Label(self.root, text='Unemployment %:').grid(row=7, column=0, sticky='e')
        self.unemployment_var = tk.DoubleVar()
        tk.Entry(self.root, textvariable=self.unemployment_var).grid(row=7, column=1)

        # Predict Button
        tk.Button(self.root, text='Predict', command=self.predict_sales).grid(row=8, column=0, columnspan=2, pady=10)

    def predict_sales(self):
        # Collect input data
        input_data = {
            'Product Calorie': self.calorie_var.get(),
            'Promotion Applied': self.promo_var.get(),
            'Day': self.day_var.get(),
            'StoreID': self.store_var.get(),
            'Product Name': self.product_var.get(),
            'Weather': self.weather_var.get(),
            'Inflation %': self.inflation_var.get(),
            'Unemployment %': self.unemployment_var.get(),
        }
        # Placeholder: Load model and columns, preprocess input, predict, and show result
        try:
            if not os.path.exists(MODEL_PATH) or not os.path.exists(COLUMNS_PATH):
                messagebox.showerror('Error', 'Model or columns file not found.')
                return
            model = joblib.load(MODEL_PATH)
            model_columns = joblib.load(COLUMNS_PATH)
            # Preprocess input (one-hot encoding, fill missing columns, etc.)
            df = pd.DataFrame([input_data])
            df = pd.get_dummies(df)
            for col in model_columns:
                if col not in df.columns:
                    df[col] = 0
            df = df[model_columns]
            prediction = model.predict(df)[0]
            messagebox.showinfo('Prediction', f'Predicted Total Sales: {prediction:.2f}')
        except Exception as e:
            messagebox.showerror('Error', str(e))

def main():
    root = tk.Tk()
    app = SalesPredictionApp(root)
    root.mainloop()

if __name__ == '__main__':
    main() 