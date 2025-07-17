import tkinter as tk
from tkinter import ttk, messagebox
import joblib
import pandas as pd
import os
import threading

# Placeholder for model and columns file paths
MODEL_PATH = 'xgb_sales_model.pkl'
COLUMNS_PATH = 'model_columns.pkl'

class SalesPredictionApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Sales Prediction App')
        self.root.geometry('500x650')
        self.root.resizable(False, False)
        self.set_dark_theme()
        self.create_widgets()

    def set_dark_theme(self):
        style = ttk.Style(self.root)
        # Use 'clam' as base for best dark support
        style.theme_use('clam')
        # Colors
        dark_bg = '#18181b'  # main background
        panel_bg = '#232329'  # panel/frame background
        accent = '#7dd3fc'   # cyan-300
        accent_hover = '#38bdf8'  # cyan-400
        entry_bg = '#27272a'
        entry_fg = '#f4f4f5'
        label_fg = '#f4f4f5'
        button_fg = '#18181b'
        button_bg = accent
        button_hover_bg = accent_hover
        border = '#52525b'
        # Root bg
        self.root.configure(bg=dark_bg)
        # Frame
        style.configure('TFrame', background=panel_bg)
        # Labels
        style.configure('TLabel', background=panel_bg, foreground=label_fg, font=('Segoe UI', 11))
        style.configure('Title.TLabel', font=('Segoe UI', 17, 'bold'), foreground=accent, background=panel_bg)
        # Entry
        style.configure('TEntry', fieldbackground=entry_bg, foreground=entry_fg, bordercolor=border, borderwidth=1, relief='flat', font=('Segoe UI', 11))
        # Combobox
        style.configure('TCombobox', fieldbackground=entry_bg, background=entry_bg, foreground=entry_fg, bordercolor=border, borderwidth=1, font=('Segoe UI', 11))
        style.map('TCombobox', fieldbackground=[('readonly', entry_bg)], foreground=[('readonly', entry_fg)])
        # Checkbutton
        style.configure('TCheckbutton', background=panel_bg, foreground=label_fg, font=('Segoe UI', 11))
        # Button
        style.configure('Accent.TButton', font=('Segoe UI', 12, 'bold'), foreground=button_fg, background=button_bg, borderwidth=0, padding=8)
        style.map('Accent.TButton', background=[('active', button_hover_bg), ('pressed', button_hover_bg)], foreground=[('active', button_fg)])

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=32, style='TFrame')
        main_frame.pack(fill='both', expand=True)

        # Title
        ttk.Label(main_frame, text='Sales Prediction', style='Title.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 24))

        # Product Calorie
        ttk.Label(main_frame, text='Product Calorie:').grid(row=1, column=0, sticky='e', pady=10, padx=(0, 12))
        self.calorie_var = tk.DoubleVar()
        calorie_entry = ttk.Entry(main_frame, textvariable=self.calorie_var, width=28, style='TEntry')
        calorie_entry.grid(row=1, column=1, pady=10)

        # Promotion Applied
        self.promo_var = tk.IntVar()
        ttk.Checkbutton(main_frame, text='Promotion Applied', variable=self.promo_var, style='TCheckbutton').grid(row=2, column=1, sticky='w', pady=10)

        # Day Dropdown
        ttk.Label(main_frame, text='Day:').grid(row=3, column=0, sticky='e', pady=10, padx=(0, 12))
        self.day_var = tk.StringVar()
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_combo = ttk.Combobox(main_frame, textvariable=self.day_var, values=days, state='readonly', width=26, style='TCombobox')
        day_combo.grid(row=3, column=1, pady=10)

        # StoreID Dropdown
        ttk.Label(main_frame, text='StoreID:').grid(row=4, column=0, sticky='e', pady=10, padx=(0, 12))
        self.store_var = tk.StringVar()
        stores = ['S001', 'S002', 'S003']
        store_combo = ttk.Combobox(main_frame, textvariable=self.store_var, values=stores, state='readonly', width=26, style='TCombobox')
        store_combo.grid(row=4, column=1, pady=10)

        # Product Name Dropdown
        ttk.Label(main_frame, text='Product Name:').grid(row=5, column=0, sticky='e', pady=10, padx=(0, 12))
        self.product_var = tk.StringVar()
        products = ['VBurger']
        product_combo = ttk.Combobox(main_frame, textvariable=self.product_var, values=products, state='readonly', width=26, style='TCombobox')
        product_combo.grid(row=5, column=1, pady=10)

        # Weather Dropdown
        ttk.Label(main_frame, text='Weather:').grid(row=6, column=0, sticky='e', pady=10, padx=(0, 12))
        self.weather_var = tk.StringVar()
        weathers = ['cold', 'hot', 'humid', 'rainy', 'very hot']
        weather_combo = ttk.Combobox(main_frame, textvariable=self.weather_var, values=weathers, state='readonly', width=26, style='TCombobox')
        weather_combo.grid(row=6, column=1, pady=10)

        # Inflation %
        ttk.Label(main_frame, text='Inflation %:').grid(row=7, column=0, sticky='e', pady=10, padx=(0, 12))
        self.inflation_var = tk.DoubleVar()
        inflation_entry = ttk.Entry(main_frame, textvariable=self.inflation_var, width=28, style='TEntry')
        inflation_entry.grid(row=7, column=1, pady=10)

        # Unemployment %
        ttk.Label(main_frame, text='Unemployment %:').grid(row=8, column=0, sticky='e', pady=10, padx=(0, 12))
        self.unemployment_var = tk.DoubleVar()
        unemployment_entry = ttk.Entry(main_frame, textvariable=self.unemployment_var, width=28, style='TEntry')
        unemployment_entry.grid(row=8, column=1, pady=10)

        # Predict Button
        predict_btn = ttk.Button(main_frame, text='Predict', command=self.on_predict_click, style='Accent.TButton')
        predict_btn.grid(row=9, column=0, columnspan=2, pady=(24, 0), sticky='ew')
        self.predict_btn = predict_btn

        # Sample Data Button
        sample_btn = ttk.Button(main_frame, text='Fill Sample Data', command=self.fill_sample_data, style='TButton')
        sample_btn.grid(row=10, column=0, pady=(16, 0), sticky='ew')
        # Clear Form Button
        clear_btn = ttk.Button(main_frame, text='Clear Form', command=self.clear_form, style='TButton')
        clear_btn.grid(row=10, column=1, pady=(16, 0), sticky='ew')

        # Spinner (Progressbar)
        self.spinner = ttk.Progressbar(main_frame, mode='indeterminate', style='TProgressbar')
        self.spinner.grid(row=11, column=0, columnspan=2, pady=(16, 0), sticky='ew')
        self.spinner.grid_remove()

        # Add some stretch to columns
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=2)

    def on_predict_click(self):
        if self.is_form_empty():
            messagebox.showerror('Error', 'Please fill in all required fields before predicting.')
            return
        self.predict_btn.state(['disabled'])
        self.spinner.grid()
        self.spinner.start(10)
        thread = threading.Thread(target=self._predict_sales_async_thread)
        thread.start()

    def is_form_empty(self):
        # Check if all fields are empty or not filled
        if (
            self.calorie_var.get() == 0.0 and
            self.promo_var.get() == 0 and
            self.day_var.get() == '' and
            self.store_var.get() == '' and
            self.product_var.get() == '' and
            self.weather_var.get() == '' and
            self.inflation_var.get() == 0.0 and
            self.unemployment_var.get() == 0.0
        ):
            return True
        # Also check for any required field being empty
        required_fields = [self.day_var.get(), self.store_var.get(), self.product_var.get(), self.weather_var.get()]
        if any(f == '' for f in required_fields):
            return True
        return False

    def _predict_sales_async_thread(self):
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
        try:
            if not os.path.exists(MODEL_PATH) or not os.path.exists(COLUMNS_PATH):
                self.root.after(0, lambda: messagebox.showerror('Error', 'Model or columns file not found.'))
                return
            model = joblib.load(MODEL_PATH)
            model_columns = joblib.load(COLUMNS_PATH)
            df = pd.DataFrame([input_data])
            df = pd.get_dummies(df)
            for col in model_columns:
                if col not in df.columns:
                    df[col] = 0
            df = df[model_columns]
            prediction = model.predict(df)[0]
            self.root.after(0, lambda: messagebox.showinfo('Prediction', f'Predicted Total Sales: {prediction:.2f}'))
            self.root.after(0, self.clear_form)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror('Error', str(e)))
        finally:
            self.root.after(0, self._on_prediction_done)

    def _on_prediction_done(self):
        self.spinner.stop()
        self.spinner.grid_remove()
        self.predict_btn.state(['!disabled'])

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
            self.clear_form()
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def clear_form(self):
        self.calorie_var.set(0.0)
        self.promo_var.set(0)
        self.day_var.set('')
        self.store_var.set('')
        self.product_var.set('')
        self.weather_var.set('')
        self.inflation_var.set(0.0)
        self.unemployment_var.set(0.0)

    def fill_sample_data(self):
        self.calorie_var.set(250.0)
        self.promo_var.set(1)
        self.day_var.set('Monday')
        self.store_var.set('S001')
        self.product_var.set('VBurger')
        self.weather_var.set('hot')
        self.inflation_var.set(5.5)
        self.unemployment_var.set(3.2)

def main():
    root = tk.Tk()
    app = SalesPredictionApp(root)
    root.mainloop()

if __name__ == '__main__':
    main() 