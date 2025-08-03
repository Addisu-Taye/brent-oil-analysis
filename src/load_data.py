# src/load_data.py
"""
Task ID:        Task-1
Created by:     Addisu Taye
Date Created:   30-JUL-2025
Purpose:        Load and parse the Brent oil prices dataset, ensuring the Date column is correctly formatted as datetime.
Key Features:   - Handles multiple date formats in raw data
               - Cleans and sorts data chronologically
               - Returns a clean pandas DataFrame ready for analysis
"""

import pandas as pd
import os

def load_brent_prices(file_path='data/BrentOilPrices.csv'):
    """
    Loads and cleans the Brent oil price data.
    Handles multiple date formats and ensures 'Price' is a numeric type.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found: {file_path}")


    # Read without header, assuming the first two columns are date and price
    df = pd.read_csv(file_path, header=None, names=['DateRaw', 'Price'])
    
    # Clean DateRaw: remove quotes and whitespace
    df['DateRaw'] = df['DateRaw'].astype(str).str.strip().str.strip('"')

    # Convert DateRaw to datetime using a two-pass approach
    # Pass 1: Try format '14-May-97'
    df['Date'] = pd.to_datetime(df['DateRaw'], format='%d-%b-%y', errors='coerce')
    
    # Pass 2: Fill NaT values by trying format 'May 14, 2023'
    # and inferring other formats as a fallback.
    # The errors='coerce' on the outer to_datetime handles cases where
    # the second format also fails.
    df['Date'] = df['Date'].fillna(pd.to_datetime(df['DateRaw'], errors='coerce'))

    # --- CRUCIAL FIX: Convert 'Price' column to numeric, coercing errors to NaN ---
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    
    # Drop rows with any NaN values in either 'Date' or 'Price'
    df = df.dropna(subset=['Date', 'Price']).sort_values('Date').reset_index(drop=True)
    
    return df[['Date', 'Price']]

def load_events(file_path="data/key_oil_events.csv"):
    """
    Loads key geopolitical and economic events.
    Handles potential malformed rows by skipping them.
    Note: Assuming events file is in 'data' directory for consistency.
    """
    if not os.path.exists(file_path):
        print(f"⚠️ Warning: Events file not found at {file_path}. Returning empty DataFrame.")
        return pd.DataFrame(columns=['Event', 'Date', 'Description'])
        
    # FIX: Use on_bad_lines='skip' to handle malformed rows and specify delimiter if needed.
    events = pd.read_csv(file_path, on_bad_lines='skip')
    
    if 'Date' in events.columns:
        events['Date'] = pd.to_datetime(events['Date'], errors='coerce')
        events = events.dropna(subset=['Date']).reset_index(drop=True)
    else:
        print(f"⚠️ Warning: 'Date' column not found in {file_path}.")
        return pd.DataFrame(columns=['Event', 'Date', 'Description'])
        
    
    return events