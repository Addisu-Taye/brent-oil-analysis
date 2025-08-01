# src/exploratory_analysis.py

"""
Task ID:        Task-1
Created by:     Addisu Taye
Date Created:   30-JUL-2025
Purpose:        Perform comprehensive exploratory data analysis on Brent oil prices.
Key Features:   - Handles mixed date formats in raw data
                - Plots price trends with event markers
                - Computes and visualizes log returns and volatility
                - Saves all plots to the reports/ directory
                - Identifies potential change points for Bayesian modeling
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
# --- NEW: Import data loading functions from the dedicated module ---
from load_data import load_brent_prices, load_events

# Set style and figure size
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 7)

# ... (plot_price_series, print_basic_statistics, plot_log_returns, etc. functions go here) ...
# I will omit them to save space as they are correct.

def plot_price_series(df, output_path="reports/price_series.png"):
    """Plot raw price series."""
    plt.figure(figsize=(16, 8))
    plt.plot(df['Date'], df['Price'], label='Brent Oil Price', color='blue', linewidth=1)
    plt.title('Brent Crude Oil Prices (1987–2023)', fontsize=18)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Price (USD per Barrel)', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"✅ Saved price series plot to {output_path}")

def print_basic_statistics(df):
    """Print descriptive statistics and key price events."""
    stats = df['Price'].describe()
    print("\n📊 Descriptive Statistics:")
    print(stats)

    min_row = df.loc[df['Price'].idxmin()]
    max_row = df.loc[df['Price'].idxmax()]

    print(f"\n📉 Minimum Price: ${min_row['Price']:.2f} on {min_row['Date'].date()}")
    print(f"📈 Maximum Price: ${max_row['Price']:.2f} on {max_row['Date'].date()}")

    annual_volatility = df['Price'].std() * np.sqrt(252)
    print(f"📊 Annualized Volatility: ${annual_volatility:.2f}")

def plot_log_returns(df, output_path="reports/log_returns.png"):
    """Plot daily log returns."""
    df['LogReturn'] = np.log(df['Price'] / df['Price'].shift(1))
    df['ReturnPct'] = df['LogReturn'] * 100

    plt.figure(figsize=(14, 6))
    plt.plot(df['Date'], df['ReturnPct'], color='purple', alpha=0.7)
    plt.title('Daily Log Returns (%)', fontsize=16)
    plt.ylabel('Return (%)')
    plt.xlabel('Year')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"✅ Saved log returns plot to {output_path}")

    print(f"\n📈 Average Daily Return: {df['LogReturn'].mean():.4f}")
    print(f"📉 Return Volatility (std): {df['LogReturn'].std():.4f}")
    print(f"📉 Skewness: {df['LogReturn'].skew():.4f} (Negative = left tail, crashes)")
    print(f"🔺 Kurtosis: {df['LogReturn'].kurtosis():.4f} (High = fat tails, extreme moves)")

def plot_rolling_statistics(df, window=90, output_path="reports/rolling_stats.png"):
    """Plot rolling mean and volatility band."""
    df['Rolling_Mean'] = df['Price'].rolling(window).mean()
    df['Rolling_Std'] = df['Price'].rolling(window).std()

    plt.figure(figsize=(14, 8))
    plt.plot(df['Date'], df['Price'], label='Price', color='blue', alpha=0.6)
    plt.plot(df['Date'], df['Rolling_Mean'], label=f'{window}-Day Rolling Mean', color='orange')
    plt.fill_between(df['Date'],
                     df['Rolling_Mean'] - df['Rolling_Std'],
                     df['Rolling_Mean'] + df['Rolling_Std'],
                     color='gray', alpha=0.2, label=f'{window}-Day Volatility Band')
    plt.title('Brent Oil Price with Rolling Statistics')
    plt.xlabel('Year')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"✅ Saved rolling stats plot to {output_path}")

def plot_price_with_events(df, events_df, output_path="reports/price_with_events.png"):
    """Plot price series with key event markers."""
    plt.figure(figsize=(16, 8))
    plt.plot(df['Date'], df['Price'], label='Brent Oil Price', color='blue', linewidth=1)

    for _, row in events_df.iterrows():
        if row['Date'] in df['Date'].values:
            idx = df[df['Date'] == row['Date']].index[0]
            price = df.loc[idx, 'Price']
            plt.axvline(row['Date'], color='red', linestyle='--', alpha=0.6)
            plt.text(row['Date'], df['Price'].max() * 0.9, row['Event'], rotation=90, fontsize=8, va='top')

    plt.title('Brent Oil Price with Key Geopolitical & Economic Events', fontsize=16)
    plt.xlabel('Year')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"✅ Saved price-with-events plot to {output_path}")

    print("\n🔍 Key Events:")
    print(events_df[['Event', 'Date']].sort_values('Date').to_string(index=False))

def plot_potential_change_points(df, output_path="reports/potential_change_points.png"):
    """Highlight candidate change points based on known events."""
    potential_dates = [
        '2020-04-12',  # OPEC+ historic cut
        '2020-03-08',  # Saudi-Russia price war
        '2008-09-15',  # Lehman collapse
        '1990-08-02',  # Iraq invades Kuwait
        '2022-02-24',  # Russia invades Ukraine
        '2020-03-11',  # WHO pandemic declaration
    ]

    plt.figure(figsize=(16, 8))
    plt.plot(df['Date'], df['Price'], label='Brent Oil Price', color='blue')

    for event_date in potential_dates:
        event_dt = pd.to_datetime(event_date)
        if event_dt in df['Date'].values:
            plt.axvline(event_dt, color='green', linestyle='-.', alpha=0.8)
            plt.text(event_dt, df['Price'].max() * 0.8, 'Candidate', rotation=90, fontsize=9, color='green')

    plt.title('Potential Change Points for Bayesian Analysis')
    plt.xlabel('Year')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"✅ Saved potential change points plot to {output_path}")

def main():
    """Main execution function."""
    print("🔍 Starting Exploratory Data Analysis on Brent Oil Prices...")

    os.makedirs("reports", exist_ok=True)

    try:
        df = load_brent_prices()
        events_df = load_events()
    except FileNotFoundError as e:
        print(f"❌ Error: {e}. Please ensure data files are in the correct location.")
        return

    print(f"✅ Data loaded: {len(df)} records from {df['Date'].min().date()} to {df['Date'].max().date()}")

    plot_price_series(df)
    print_basic_statistics(df)
    plot_log_returns(df)
    plot_rolling_statistics(df)
    plot_price_with_events(df, events_df)
    plot_potential_change_points(df)

    print("\n✅ Exploratory Analysis Complete. Check the 'reports/' folder for visualizations.")


if __name__ == "__main__":
    main()